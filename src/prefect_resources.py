#!/usr/bin/env python3


"""Define Prefect tasks and flows."""

import shutil
from pathlib import Path
from typing import List

from prefect import flow, get_run_logger, task
from prefect_dbt import PrefectDbtRunner, PrefectDbtSettings


@task(log_prints=True)
def clean_dbt_outputs(
    project_dir: Path,
    folders_to_delete: List[str] | None = None,
    files_to_delete: List[str] | None = None,
) -> None:
    """Deletes specified files and folders from the dbt project directory.

    Files and folders are deleted using the paths relative to the dbt
    project directory. Missing files and folders are ignored. Default
    cleanup targets are ``package-lock.yml``,
    ``local_warehouse.duckdb``, and ``__pycache__``.

    Args:
        project_dir: The path to the dbt project directory.
        folders_to_delete: The folder names to delete. Defaults to
            ``__pycache__``.
        files_to_delete: The filenames to delete. Defaults to
            ``package-lock.yml`` and ``local_warehouse.duckdb``.

    Returns:
        None: The function deletes the specified files and folders and
            does not return a value.
    """
    logger = get_run_logger()

    if files_to_delete is None:
        files_to_delete = ["package-lock.yml", "local_warehouse.duckdb"]
    for filename in files_to_delete:
        path = project_dir / filename
        path_base_str = f"{project_dir.stem}/{path.name}"
        logger.info(f"Cleaning file at {path_base_str}")
        path.unlink(missing_ok=True)
        logger.info(f"Cleaned file at {path_base_str}")

    if folders_to_delete is None:
        folders_to_delete = ["__pycache__"]
    for folder in folders_to_delete:
        path = project_dir / folder
        path_base_str = f"{project_dir.stem}/{path.name}"
        logger.info(f"Cleaning folder at {path_base_str}")
        shutil.rmtree(path, ignore_errors=True)
        logger.info(f"Cleaned folder at {path_base_str}")


@task(retries=0, retry_delay_seconds=5, log_prints=True)
def run_dbt_commands(
    commands: List[str], project_dir: Path, profiles_dir: Path
) -> None:
    """Runs dbt commands sequentially using the Prefect dbt integration.

    Each command is passed to ``PrefectDbtRunner`` for execution using the
    specified dbt project and profiles directories. A failed command
    raises an exception and stops execution of subsequent commands.

    The task has retries disabled, so a failed dbt command is not retried
    by Prefect.

    Args:
        commands: The dbt commands to execute, without the leading
            ``dbt`` command. Each command may contain command-line
            arguments.
        project_dir: The path to the dbt project directory.
        profiles_dir: The path to the directory containing the dbt
            ``profiles.yml`` file.

    Returns:
        None: The function executes the specified dbt commands and does
            not return a value.

    Raises:
        Exception: If a dbt command fails during execution.

    Examples:
        >>> run_dbt_commands(
        ...     commands=["run", "test"],
        ...     project_dir=Path("./dbt"),
        ...     profiles_dir=Path("./dbt"),
        ... )
    """
    print(f"Running dbt commands: {commands}\n")

    # Configure dbt settings to point to project directory
    settings = PrefectDbtSettings(
        project_dir=str(project_dir),
        profiles_dir=str(profiles_dir),
    )

    # Create runner and execute commands. `raise_on_failure=True` (the
    # default) turns any failed dbt node into a Python exception, which
    # triggers the enclosing Prefect task's retries and marks the task
    # and ultimately the flow as Failed if the retries are exhausted.
    runner = PrefectDbtRunner(settings=settings)

    for command in commands:
        print(f"Executing: dbt {command}")
        runner.invoke(command.split())
        print(f"Completed: dbt {command}\n")


@flow(name="dbt_prefect_starter_flow", log_prints=True)
def dbt_flow(
    commands: List[str], project_dir: Path, profiles_dir: Path
) -> None:
    """Runs dbt commands as a Prefect flow.

    The flow passes all commands to ``run_dbt_commands``, which executes
    them sequentially using the Prefect dbt integration. If the final
    command is ``clean``, the flow also removes the configured dbt
    output files and folders.

    Args:
        commands: The dbt commands to execute, without the leading
            ``dbt`` command. Each command may contain command-line
            arguments.
        project_dir: The path to the dbt project directory.
        profiles_dir: The path to the directory containing the dbt
            ``profiles.yml`` file.

    Returns:
        None: The flow executes the specified dbt commands and does not
            return a value.

    Raises:
        Exception: If a dbt command fails during execution.

    Examples:
        >>> dbt_flow(
        ...     commands=["run", "test"],
        ...     project_dir=Path("./dbt"),
        ...     profiles_dir=Path("./dbt"),
        ... )
    """
    cmd_str = f"[{', '.join(commands)}]"
    logger = get_run_logger()
    logger.info(
        f"Starting flow execution for {len(commands)} command(s): {cmd_str}"
    )
    run_dbt_commands(commands, project_dir, profiles_dir)
    if "clean" in commands and commands[-1] == "clean":
        clean_dbt_outputs(
            project_dir=project_dir,
            folders_to_delete=["__pycache__"],
            files_to_delete=["package-lock.yml", "local_warehouse.duckdb"],
        )
    logger.info(f"Completed flow to execute {len(commands)} command(s)")
