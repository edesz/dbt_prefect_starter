#!/usr/bin/env python3


"""Test Prefect tasks."""

from pathlib import Path
from unittest.mock import MagicMock, call, patch

from src.prefect_resources import clean_dbt_outputs, run_dbt_commands


def test_clean_dbt_outputs_removes_default_files_and_folders(
    tmp_path: Path,
) -> None:
    """Deletes the default dbt output files and folders."""
    files = [
        "package-lock.yml",
        "local_warehouse.duckdb",
    ]
    folders = ["__pycache__"]

    for filename in files:
        (tmp_path / filename).touch()

    for folder in folders:
        (tmp_path / folder).mkdir()

    clean_dbt_outputs(project_dir=tmp_path)

    for filename in files:
        assert not (tmp_path / filename).exists()

    for folder in folders:
        assert not (tmp_path / folder).exists()


def test_clean_dbt_outputs_ignores_missing_targets(
    tmp_path: Path,
) -> None:
    """Does not raise an error when cleanup targets are missing."""
    clean_dbt_outputs(project_dir=tmp_path)

    assert not (tmp_path / "package-lock.yml").exists()
    assert not (tmp_path / "local_warehouse.duckdb").exists()
    assert not (tmp_path / "__pycache__").exists()


def test_clean_dbt_outputs_removes_custom_files_and_folders(
    tmp_path: Path,
) -> None:
    """Deletes files and folders specified by the caller."""
    custom_file = tmp_path / "custom_file.txt"
    custom_folder = tmp_path / "custom_folder"

    custom_file.touch()
    custom_folder.mkdir()

    clean_dbt_outputs(
        project_dir=tmp_path,
        files_to_delete=["custom_file.txt"],
        folders_to_delete=["custom_folder"],
    )

    assert not custom_file.exists()
    assert not custom_folder.exists()


def test_clean_dbt_outputs_preserves_unspecified_files_and_folders(
    tmp_path: Path,
) -> None:
    """Leaves files and folders outside the cleanup targets unchanged."""
    preserved_file = tmp_path / "preserved.txt"
    preserved_folder = tmp_path / "preserved_folder"

    preserved_file.touch()
    preserved_folder.mkdir()

    clean_dbt_outputs(
        project_dir=tmp_path,
        files_to_delete=["other_file.txt"],
        folders_to_delete=["other_folder"],
    )

    assert preserved_file.exists()
    assert preserved_folder.exists()


def test_run_dbt_commands_configures_runner(
    tmp_path: Path,
) -> None:
    """Creates the dbt runner with the specified project and profiles paths."""
    project_dir = tmp_path / "dbt"
    profiles_dir = tmp_path / "profiles"

    with (
        patch("src.prefect_resources.PrefectDbtSettings") as mock_settings,
        patch("src.prefect_resources.PrefectDbtRunner") as mock_runner,
    ):
        run_dbt_commands(
            commands=["run"],
            project_dir=project_dir,
            profiles_dir=profiles_dir,
        )

    mock_settings.assert_called_once_with(
        project_dir=str(project_dir),
        profiles_dir=str(profiles_dir),
    )
    mock_runner.assert_called_once_with(
        settings=mock_settings.return_value,
    )


def test_run_dbt_commands_executes_commands_sequentially(
    tmp_path: Path,
) -> None:
    """Executes each dbt command sequentially."""
    commands = [
        "deps",
        "run",
        "test",
    ]

    mock_runner_instance = MagicMock()

    with (
        patch(
            "src.prefect_resources.PrefectDbtRunner",
            return_value=mock_runner_instance,
        ),
    ):
        run_dbt_commands(
            commands=commands,
            project_dir=tmp_path,
            profiles_dir=tmp_path,
        )

    expected_calls = [
        ("deps".split(),),
        ("run".split(),),
        ("test".split(),),
    ]

    assert mock_runner_instance.invoke.call_args_list == [
        call(*args) for args in expected_calls
    ]


def test_run_dbt_commands_splits_command_arguments(
    tmp_path: Path,
) -> None:
    """Splits command strings into arguments before invoking dbt."""
    commands = [
        "run --select staging",
        "test --select stg_bank_churners",
    ]

    mock_runner_instance = MagicMock()

    with patch(
        "src.prefect_resources.PrefectDbtRunner",
        return_value=mock_runner_instance,
    ):
        run_dbt_commands(
            commands=commands,
            project_dir=tmp_path,
            profiles_dir=tmp_path,
        )

    assert mock_runner_instance.invoke.call_args_list == [
        call(["run", "--select", "staging"]),
        call(["test", "--select", "stg_bank_churners"]),
    ]


def test_run_dbt_commands_stops_after_failed_command(
    tmp_path: Path,
) -> None:
    """Stops executing commands when a dbt command fails."""
    commands = [
        "deps",
        "run",
        "test",
    ]

    mock_runner_instance = MagicMock()
    mock_runner_instance.invoke.side_effect = [
        None,
        RuntimeError("dbt command failed"),
    ]

    with patch(
        "src.prefect_resources.PrefectDbtRunner",
        return_value=mock_runner_instance,
    ):
        try:
            run_dbt_commands(
                commands=commands,
                project_dir=tmp_path,
                profiles_dir=tmp_path,
            )
        except RuntimeError as exc:
            assert str(exc) == "dbt command failed"
        else:
            raise AssertionError("Expected RuntimeError was not raised")

    assert mock_runner_instance.invoke.call_count == 2
    assert mock_runner_instance.invoke.call_args_list == [
        call(["deps"]),
        call(["run"]),
    ]
