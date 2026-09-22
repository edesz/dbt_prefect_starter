#!/usr/bin/env python3


"""Run an ad-hoc SQL query using DuckDB."""

import argparse
import os

import duckdb

DEFAULT_DB_PATH = "./local_warehouse.duckdb"


def main():
    # Set up the CLI argument parser
    parser = argparse.ArgumentParser(
        description="Run an ad-hoc dbt analysis SQL file against DuckDB."
    )
    parser.add_argument(
        "sql_file",
        type=str,
        help="Path to the SQL file (e.g., analyses/check_toronto_csv.sql)",
    )
    parser.add_argument(
        "--db",
        type=str,
        default=DEFAULT_DB_PATH,
        help=f"Path to the DuckDB database file (default: {DEFAULT_DB_PATH})",
    )

    args = parser.parse_args()

    # Validate that the SQL file exists
    if not os.path.exists(args.sql_file):
        print(f"Error: File not found at '{args.sql_file}'")
        return

    # Read the SQL query
    with open(args.sql_file, "r") as file:
        query = file.read()

    print(f"Connecting to '{args.db}'...")
    print(f"Running query from '{args.sql_file}'...\n")

    # Connect to DuckDB and execute
    # read_only=True prevents locking issues if dbt is running concurrently
    try:
        conn = duckdb.connect(args.db, read_only=True)
        result = conn.sql(query).pl()
        print(result)
    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        if "conn" in locals():
            conn.close()


if __name__ == "__main__":
    main()
