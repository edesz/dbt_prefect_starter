#!/usr/bin/env python3


"""Use Prefect to run dbt commands."""

from pathlib import Path

import typer
from dotenv import load_dotenv

from src.prefect_resources import dbt_flow

PROJ_ROOT = Path.cwd()

project_dir = PROJ_ROOT
profiles_dir = PROJ_ROOT

assert load_dotenv(
    dotenv_path=PROJ_ROOT.parents[1] / "Documents" / ".env", override=False
)

app = typer.Typer()


@app.command()
def run(
    commands_str: str = typer.Option(
        "debug,deps,run,test,clean,docs generate,docs serve --port 8086,clean",
        "--commands",
        "-n",
        help="A comma-separated list of dbt commands to run",
    )
) -> None:
    """Parses dbt commands and executes them through the Prefect flow.

    The comma-separated command string is stripped of surrounding
    whitespace and converted to a list before being passed to
    ``dbt_flow``.

    Args:
        commands_str: The comma-separated string of dbt commands to
            execute.

    Returns:
        None: The function parses the commands and starts the Prefect
            flow without returning a value.

    Examples:
        >>> run("debug,deps,run,test,clean")
    """
    # split by comma and strip whitespace from each item
    cmds_list = [cmd.strip() for cmd in commands_str.split(",") if cmd.strip()]

    # run single Prefect task to execute each dbt command
    dbt_flow(cmds_list, project_dir, profiles_dir)


if __name__ == "__main__":
    app()
