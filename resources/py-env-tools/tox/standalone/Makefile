#################################################################################
# GLOBALS                                                                       #
#################################################################################

#################################################################################
# COMMANDS                                                                      #
#################################################################################



#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

## Run lint checks manually
lint:
	@echo "+ $@"
	@if [ ! -d .git ]; then git init && git add .; fi;
	@tox -e py313-lint
.PHONY: lint

## Run adhoc dbt command
dbt-cmd:
	@echo "+ $@"
	@tox -e py313-dbt -- "debug"
.PHONY: dbt-cmd

## Show active configuration settings for Prefect
prefect-config-view:
	@echo "+ $@"
	@tox -e py313-prefect-adhoc-command -- config view
.PHONY: prefect-config-view

## Run dbt commands with Prefect
prefect-dbt:
	@echo "+ $@"
	@tox -e py313-orchestration -- "debug,deps,run,test,docs generate"
.PHONY: prefect-dbt

## Run ad-hoc SQL queries with DuckDB
run-adhoc-query:
	@echo "+ $@"
	@tox -e py313-adhocsql -- "analyses/check_parking_occupancy_records.sql"
.PHONY: run-adhoc-query

## Run unit tests on Prefect tasks and flows with PyTest
tests:
	@echo "+ $@"
	@tox -e py313-unittests
.PHONY: tests

## Install and Upgrade uv
uv-install-upgrade:
	@echo "+ $@"
	@pip3 install --upgrade uv
.PHONY: uv-install-upgrade

## Use uv to pin Python version for working directory only
uv-pin-python:
	@echo "+ $@"
	@uv python pin 3.13.15
.PHONY: uv-pin-python

## Use uv to install tox, through the tox-uv plugin
uv-install-tox:
	@echo "+ $@"
	@uv tool install tox --with tox-uv
.PHONY: uv-install-tox

## Use uv to upgrade tox
uv-upgrade-tox:
	@echo "+ $@"
	@uv tool upgrade tox
.PHONY: uv-upgrade-tox

## Show all available tox commands
tox-help:
	@echo "+ $@"
	@tox list
.PHONY: tox-help

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
