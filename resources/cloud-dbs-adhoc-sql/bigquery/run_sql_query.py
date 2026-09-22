#!/usr/bin/env python3


"""Run an ad-hoc SQL query using BigQuery."""

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from google.cloud import bigquery


def run_bigquery_script(sql_file_path: Path) -> None:
    """Connects to BigQuery and executes a multi-statement SQL script.

    This function reads a local SQL file and runs all statements
    sequentially on Google BigQuery as a script/parent job.

    Args:
        sql_file_path: The local file path to the target SQL script.

    Raises:
        KeyError: If any required BigQuery environment variables are
            missing.
        Exception: For any database or file connection runtime errors.
    """
    # 1. Initialize the client using explicit project details
    # The client library automatically looks for credentials via the
    # GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = bigquery.Client(
        project=os.environ["BIGQUERY_PROJECT_ID"],
        location=os.environ.get("BIGQUERY_LOCATION"),  # e.g., "US"
    )

    try:
        # 2. Open and read the entire script file
        with open(sql_file_path, "r", encoding="utf-8") as f:
            sql_script = f.read()

        print(f"Running query from: {str(sql_file_path)}\n")

        # 3. Submit the entire multi-statement script to BigQuery
        query_job = client.query(sql_script)

        # Wait for the script execution to complete
        results = query_job.result()

        # 4. Enumerate completed internal child statements
        # When a script runs, BigQuery spawns a child job for each
        # distinct statement inside the file.
        child_jobs = list(client.list_jobs(parent_job=query_job.job_id))
        # Reverse list to show child jobs in order of execution
        child_jobs.reverse()

        print(f"Script job {query_job.job_id} completed successfully.")
        print(f"Executed {len(child_jobs)} internal statements:\n")

        for i, child_job in enumerate(child_jobs, start=1):
            # Clean up query text for cleaner logs
            clean_query = (
                child_job.query.strip().replace("\n", " ")
                if child_job.query
                else "PROCEDURAL BLOCK"
            )
            print(
                f"Statement {i}: {clean_query[:60]}... "
                f"[{child_job.statement_type}]"
            )

            # If the statement was a SELECT query, print rows affected
            if child_job.statement_type == "SELECT" and i == len(child_jobs):
                # Fetching rows from the final result iterator
                print(f"Final statement returned {results.total_rows} rows.")

    except Exception as e:
        print(f"An error occurred while executing the script: {e}")


if __name__ == "__main__":
    PROJ_ROOT = Path.cwd()

    assert load_dotenv(dotenv_path=PROJ_ROOT.parent / ".env")

    # Set up the CLI argument parser
    parser = argparse.ArgumentParser(
        description="Run a multi-statement SQL script against BigQuery."
    )
    parser.add_argument(
        "sql_file",
        type=str,
        help=("Path to the SQL file (e.g., " "analyses/check_toronto_csv.sql)"),
    )

    args = parser.parse_args()

    # Cast the parsed string path into a Path object
    run_bigquery_script(Path(args.sql_file))
