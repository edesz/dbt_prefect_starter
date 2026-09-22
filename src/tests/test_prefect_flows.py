#!/usr/bin/env python3

"""Test Prefect flows."""

from pathlib import Path
from unittest.mock import patch

from src.prefect_resources import dbt_flow


def test_dbt_flow_runs_dbt_commands(
    tmp_path: Path,
) -> None:
    """Runs the specified dbt commands."""
    commands = ["run", "test"]

    with patch(
        "src.prefect_resources.run_dbt_commands"
    ) as mock_run_dbt_commands:
        dbt_flow(
            commands=commands,
            project_dir=tmp_path,
            profiles_dir=tmp_path,
        )

    mock_run_dbt_commands.assert_called_once_with(
        commands,
        tmp_path,
        tmp_path,
    )


def test_dbt_flow_cleans_outputs_when_clean_is_last_command(
    tmp_path: Path,
) -> None:
    """Cleans dbt outputs when clean is the final command."""
    commands = ["run", "test", "clean"]

    with (
        patch(
            "src.prefect_resources.run_dbt_commands"
        ) as mock_run_dbt_commands,
        patch(
            "src.prefect_resources.clean_dbt_outputs"
        ) as mock_clean_dbt_outputs,
    ):
        dbt_flow(
            commands=commands,
            project_dir=tmp_path,
            profiles_dir=tmp_path,
        )

    mock_run_dbt_commands.assert_called_once_with(
        commands,
        tmp_path,
        tmp_path,
    )
    mock_clean_dbt_outputs.assert_called_once_with(
        project_dir=tmp_path,
        folders_to_delete=["__pycache__"],
        files_to_delete=[
            "package-lock.yml",
            "local_warehouse.duckdb",
        ],
    )


def test_dbt_flow_does_not_clean_when_clean_is_not_last_command(
    tmp_path: Path,
) -> None:
    """Does not clean dbt outputs when clean is not the final command."""
    commands = ["clean", "run"]

    with (
        patch(
            "src.prefect_resources.run_dbt_commands"
        ) as mock_run_dbt_commands,
        patch(
            "src.prefect_resources.clean_dbt_outputs"
        ) as mock_clean_dbt_outputs,
    ):
        dbt_flow(
            commands=commands,
            project_dir=tmp_path,
            profiles_dir=tmp_path,
        )

    mock_run_dbt_commands.assert_called_once_with(
        commands,
        tmp_path,
        tmp_path,
    )
    mock_clean_dbt_outputs.assert_not_called()


def test_dbt_flow_does_not_clean_without_clean_command(
    tmp_path: Path,
) -> None:
    """Does not clean dbt outputs when clean is not specified."""
    commands = ["run", "test"]

    with (
        patch(
            "src.prefect_resources.run_dbt_commands"
        ) as mock_run_dbt_commands,
        patch(
            "src.prefect_resources.clean_dbt_outputs"
        ) as mock_clean_dbt_outputs,
    ):
        dbt_flow(
            commands=commands,
            project_dir=tmp_path,
            profiles_dir=tmp_path,
        )

    mock_run_dbt_commands.assert_called_once_with(
        commands,
        tmp_path,
        tmp_path,
    )
    mock_clean_dbt_outputs.assert_not_called()
