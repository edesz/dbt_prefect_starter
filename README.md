# dbt Starter with Prefect Cloud

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

### Prefect Cloud Connection Profile

When using Prefect Cloud to execute flow runs, create and use a profile specifically for Cloud, which contains your `PREFECT_API_URL` and `PREFECT_API_KEY` in order to authenticate with the Prefect Cloud API using an API key.

First, get the [Prefect API settings from your Prefect Cloud account](https://docs.prefect.io/v3/how-to-guides/cloud/connect-to-cloud#manually-configure-prefect-api-settings) by following the steps below

1. Get your Prefect Cloud account ID
   - log in to your [Prefect Cloud Dashboard](https://app.prefect.cloud/auth/sign-in)
   - look at the URL in your browser's address bar. It will follow this structure: `https://prefect.cloud`
   - the string of text directly after `/account/` is your Prefect Account ID
2. Get the Prefect Cloud workspace ID. When logged into the Prefect Cloud UI and viewing your workspace dashboard, the workspace ID is embedded directly in the address bar. Look for the alphanumeric string at the end of the URL
   ```text
   https://app.prefect.cloud/account/[YOUR-ACCOUNT-ID]/workspace/[YOUR-WORKSPACE-ID]/dashboard
   ```

   where `[YOUR-ACCOUNT-ID]` is your Prefect Account ID from the previous step
3. Assemble the Prefect Cloud URL, which is the same as above but without the `/dashboard` suffix
   ```text
   https://app.prefect.cloud/account/[YOUR-ACCOUNT-ID]/workspace/[YOUR-WORKSPACE-ID]
   ```
4. [Create a Prefect Cloud API key](https://docs.prefect.io/v3/how-to-guides/cloud/manage-users/api-keys#create-an-api-key)
   - go to the Prefect Cloud Login and sign in
   - slick on your Profile Avatar or image in the bottom-left corner
   - select *Settings* from the menu
   - click on API Keys in the settings sidebar
   - click the *+ Create API Key* (or *Generate API Key*) button
   - enter a name for the key and choose an expiration date (e.g. 30 days, 90 days, or never)
   - click *Create* and copy the key immediately since it will only be shown to you once

Next, create a file at `~/.prefect/profiles.toml` with the two environment variables from above as follows

```toml
active = "cloud"

[profiles.default]

[profiles.local]

[profiles.cloud]
PREFECT_API_KEY = "<your-Prefect-Cloud-api-key-here>"
PREFECT_API_URL = "<your-Prefect-Cloud-url-here>"
```

It is important to ensure `active` is set to `"cloud"` in order to use your Prefect Cloud account.

Note that a local profile is only helpful if you also want the convenience of easily switching back to a local instance (like *http://127.0.0.1:4200/api*) on your machine. If you never run Prefect locally, you don't need it. Here, we are using Prefect Cloud so we do not need the following

```toml
[profiles.local]
PREFECT_API_URL = "<your-Prefect-Server-url-here>"
```

## Usage

### Fork Repository

Navigate to the repository on GitHub and click the *Fork* button in the top-right corner.

### Clone Repository

Copy your new fork's URL and clone it locally

```bash
git clone https://github.com/<your-github-user-name>/dbt_prefect_starter.git
```

Configure the Prefect API settings as Secrets on your Github repository

```text
PREFECT_API_URL
```

and

```text
PREFECT_API_KEY
```

### Change into Project Directory

Change into the root directory of the cloned repository. All commands are run from this location.

### Orchetrate dbt Workflow with Prefect Cloud

Use Prefect to run the following dbt commands in order

```bash
dbt debug
dbt deps
dbt run
dbt test
dbt docs generate
```

by running the following

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
pixi-self-update    Update pixi 
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

tox [environments](https://tox.wiki/en/stable/tutorial/getting-started.html#environment-settings) and [commands](https://tox.wiki/en/stable/tutorial/getting-started.html#understanding-the-configuration) are defined in [`tox.toml`](https://tox.wiki/en/stable/reference/config.html#discovery-and-file-types) found at [`pyresources/tox/using-uv/TOML/tox.toml`](./pyresources/py-env-tools/tox/using-uv/tox.toml).

Additional files required when using tox are

1. [`pyresources/py-env-tools/tox/using-uv/.gitignore`](./resources/py-env-tools/tox/using-uv/.gitignore)
2. [`pyresources/py-env-tools/tox/using-uv/pyproject.toml`](./resources/py-env-tools/tox/using-uv/pyproject.toml)
3. [`pyresources/py-env-tools/tox/using-uv/TOML/Makefile`](./resources/py-env-tools/tox/using-uv/TOML/Makefile)

These three files should replace the corresponding files in the root directory of the project since they support Pixi by default.

Currently, `tox` is configured using both the INI format, which has been deprecated, and the [newer TOML format](https://tox.wiki/en/stable/reference/config.html#discovery-and-file-types). If switching to the `tox` approach, use the TOML format only.
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
