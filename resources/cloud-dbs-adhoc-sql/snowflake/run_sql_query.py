#!/usr/bin/env python3


"""Run an ad-hoc SQL query using Snowflake."""

import argparse
import os
from pathlib import Path

import snowflake.connector
from dotenv import load_dotenv


def run_snowflake_script(sql_file_path: Path) -> None:
    """Connects to Snowflake and executes a multi-statement SQL script.

    This function reads a local SQL file, splits it into separate
    statements, and runs them sequentially on Snowflake using environment
    variables for authentication.

    Args:
        sql_file_path: The local file path to the target SQL script.

    Raises:
        KeyError: If any required Snowflake environment variables are
            missing.
        Exception: For any database or file connection runtime errors.
    """
    # Establish the connection using strict environment variables
    conn = snowflake.connector.connect(
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        database=os.environ["SNOWFLAKE_DATABASE"],
        schema=os.environ["SNOWFLAKE_SCHEMA"],
        role=os.environ["SNOWFLAKE_ROLE"],
    )

    try:
        # Open the file and execute the stream of statements
        with open(sql_file_path, "r", encoding="utf-8") as f:
            # execute_stream returns an iterator of cursors
            cursor_list = conn.execute_stream(f)

            print(f"Running query from: {str(sql_file_path)}\n")

            # Iterate through cursors to process results
            for i, cursor in enumerate(cursor_list, start=1):
                # Clean up query text for cleaner logs
                clean_query = cursor.query.strip().replace("\n", " ")
                print(f"Executing statement {i}: " f"{clean_query[:60]}...")

                if cursor.description:
                    results = cursor.fetchall()
                    print(f"Statement {i} returned {len(results)} rows.")
                else:
                    print(
                        f"Statement {i} completed. Rows affected: "
                        f"{cursor.rowcount}"
                    )
    except Exception as e:
        print(f"An error occurred while executing the script: {e}")
    finally:
        # Close connection
        conn.close()
        print("\nSnowflake connection closed.")


if __name__ == "__main__":
    PROJ_ROOT = Path.cwd()

    assert load_dotenv(dotenv_path=PROJ_ROOT.parent / ".env")

    # Set up the CLI argument parser
    parser = argparse.ArgumentParser(
        description="Run a multi-statement SQL script against Snowflake."
    )
    parser.add_argument(
        "sql_file",
        type=str,
        help=(
            "Path to the SQL file (e.g., "
            "analyses/check_parking_occupancy_records.sql)"
        ),
    )

    args = parser.parse_args()

    # Cast the parsed string path into a Path object
    run_snowflake_script(Path(args.sql_file))
