# dbt Starter with Prefect

[![CI](https://github.com/edesz/dbt_prefect_starter/actions/workflows/main.yml/badge.svg)](https://github.com/edesz/dbt_prefect_starter/actions/workflows/main.yml) ![Static Badge](https://img.shields.io/badge/MIT-License?style=for-the-badge&label=LICENSE&color=%2326ED46) ![Python](https://img.shields.io/badge/python-%233670A0.svg?style=for-the-badge&logo=python&logoColor=ffdd54) ![Maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg) ![GitHub stars](https://img.shields.io/github/stars/edesz/dbt_prefect_starter) 

This project is a starter template for [dbt](https://www.getdbt.com/) data modeling.

The stack used is

1. [Prefect](https://www.prefect.io/) is used as the orchestrator
2. [DuckDB](https://duckdb.org/) is used as the (local) data warehouse
3. [Pixi](https://pixi.prefix.dev/latest/) is used to handle Python virtual environments

## Getting Started

### Pre-Requisites

1. [Python](https://www.python.org/) ([installation](https://www.python.org/downloads/))
2. [Pixi](https://pixi.prefix.dev/latest/) ([installation](https://pixi.prefix.dev/latest/installation/))
3. [Git](https://git-scm.com/) ([installation](https://git-scm.com/install/))
4. [Make](https://www.gnu.org/software/make/) ([installation](https://www.gnu.org/software/make/#download))
5. Create an account on [Prefect Cloud](https://www.prefect.io/prefect/cloud)

### Environment Variables

Get the [Prefect API settings](https://docs.prefect.io/v3/how-to-guides/cloud/connect-to-cloud#manually-configure-prefect-api-settings)

#### Local

Configure `~/.prefect/profiles.yml` as follows

```yaml
active = "cloud"

[profiles.default]

[profiles.local]
PREFECT_API_URL = "your-Prefect-Server-url-here"

[profiles.cloud]
PREFECT_API_KEY = "your-Prefect-Cloud-api-key-here"
PREFECT_API_URL = "your-Prefect-Cloud-url-here"
```

It is important to ensure `active` is set to `"cloud"` in order to use your Prefect Cloud account.

#### Repository

Configure the Prefect API settings as Secrets on your Github repository

```text
PREFECT_API_URL
```

and

```text
PREFECT_API_KEY
```

## Usage

### Clone Repo

```bash
git clone https://github.com/edesz/dbt_prefect_starter.git
```

### Orchetrate dbt Workflow

Run the following dbt commands in order

```bash
dbt debug
dbt deps
dbt run
dbt test
dbt docs generate
```

by running the following commands from the root directory of the project

```bash
make prefect-dbt
```

### Run Ad-Hoc SQL Script

1. Create a `.sql` script in `analyses/` containing the ad-hoc SQL query.
2. In `Makefile` change the name of the `.sql` file in the `analyses` subfolder to the name of the script to be run.
3. Run the ad-hoc SQL query using
   ```bash
   make run-adhoc-query
   ```

## Additional Functionality

Below are a full list of [`make` rules](https://web.mit.edu/gnu/doc/html/make_4.html)

```bash
Available rules:

dbt-cmd             Run adhoc dbt command 
lint                Run lint checks manually 
pixi-help           Show all available pixi commands 
pixi-upgrade        Upgrade package versions with pixi 
prefect-config-view Show active configuration settings for Prefect 
prefect-dbt         Run dbt commands with Prefect 
run-adhoc-query     Run ad-hoc SQL query 
tests               Run unit tests on Prefect tasks and flows with PyTest
```

To see a full list of the `make` rules, use

```bash
make help
```

## Development Notes

<details>
<summary><b>Configuration File Formats</b></summary>

For managing Python environments, two Python environment management options are available

<details>
<summary><b>Pixi</b></summary>

(default) As [mentioned above](#pre-requisites), Pixi is used to manage Python environments.

Pixi [environments](https://pixi.prefix.dev/latest/workspace/multi_environment/#environment-feature-definitions) and [tasks](https://pixi.prefix.dev/latest/getting_started/#tasks) are configured in [`pyproject.toml`](https://pixi.prefix.dev/latest/python/tutorial/#pixitoml-and-pyprojecttoml)
  
For convenience, Pixi tasks defined in [`pyresources/py-env-tools/pixi/pyproject.toml`](./pyresources/py-env-tools/pixi/pyproject.toml) are called using a `Makefile` at [`pyresources/py-env-tools/pixi/Makefile`](./pyresources/py-env-tools/pixi/Makefile).

</details>

<details>
<summary><b>Tox</b></summary>

[`tox`](https://tox.wiki/en/stable/) can be used instead of Pixi to manage Python environments. By using the [`tox-uv` plugin](https://github.com/tox-dev/tox-uv#tox-uv), `tox` can be used with [`uv`](https://docs.astral.sh/uv/) in order to realise performance improvements compared to the default `virtualenv`.

tox [environments](https://tox.wiki/en/stable/tutorial/getting-started.html#environment-settings) and [commands](https://tox.wiki/en/stable/tutorial/getting-started.html#understanding-the-configuration) are defined in [`tox.ini`](https://tox.wiki/en/stable/reference/config.html#discovery-and-file-types)

As with Pixi, tox commands defined in [`pyresources/tox/tox.ini`](./pyresources/py-env-tools/tox/tox.ini) can be called using the `Makefile` at [`pyresources/py-env-tools/tox/Makefile`](./resources/py-env-tools/tox/Makefile).

Currently, `tox` is configured using the INI format, which has been deprecated in favour of the TOML format ([link](https://tox.wiki/en/stable/reference/config.html#discovery-and-file-types)). Future work should translate [`pyresources/py-env-tools/tox/tox.ini`](./pyresources/py-env-tools/tox/tox.ini) into the TOML format.
</details>
</details>

## Limitations

<details>
<summary><b>pre-commit Hook</b></summary>

The [pre-commit `dbt-checkpoint` hook](https://github.com/dbt-checkpoint/dbt-checkpoint) excludes the [`check-source-has-all-columns` hook](https://github.com/dbt-checkpoint/dbt-checkpoint/blob/main/HOOKS.md#check-source-has-all-columns).

The source table `parking_lot_occupancies` defined in `models/staging/stg_*/*__sources.yml` is configured to read dynamically from an external URL via DuckDB's `read_csv_auto`. Because we are using the [`dbt-duckdb` adapter](https://github.com/duckdb/dbt-duckdb) with an external CSV URL, the source data does not physically live inside a persistent database catalog. Instead, dbt goes directly to the staging model, executes the `read_csv_auto` query against the web URL on the fly, cleans column names (change to lowercase), and writes that transformed data into a physical view inside the `local_warehouse.duckdb` file. As a result, it never copies the raw data or creates a schema structure for the raw source defined in `*__sources.yml` inside the `.duckdb` file. The database only contains the final staging model.

When `dbt docs generate` executes, even when running successfully inside pre-commit, DuckDB evaluates the configuration but completely ignores external read streams (like `read_csv_auto`) when generating the formal `target/catalog.json` schema. Since the raw `parking_lot_occupancies` source table is just a pointer to a URL, it has no physical entry inside DuckDB's database tables. So, DuckDB leaves it out of the response, dbt leaves it out of `target/catalog.json`. As a result, the source details are completely missing from the generated catalog, and this hook fails. The `check-source-has-all-columns` pre-commit hook crashes.

This hook is explicitly designed for traditional databases (like Snowflake or BigQuery) where a physical table structure always exists to compare against the `.yml` file. For an in-memory, file-based adapter like `dbt-duckdb`, this check will never pass in an automated framework.
</details>

  --------
