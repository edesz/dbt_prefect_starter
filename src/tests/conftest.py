#!/usr/bin/env python3


"""Define pytest fixtures."""

import os
from typing import Generator

import pytest
from prefect.testing.utilities import prefect_test_harness


@pytest.fixture(autouse=True, scope="session")
def prefect_api_harness(
    server_startup_timeout: int = 60,
) -> Generator[None, None, None]:
    """Provides an isolated, ephemeral Prefect API and database instance.

    This fixture uses Prefect's built-in test harness to spin up a temporary,
    in-memory database and API server. It ensures that all tests running within
    the session scope execute in isolation, preventing them from modifying or
    interacting with production Prefect servers or active local databases.

    Args:
        server_startup_timeout: The maximum number of seconds to wait for
            the ephemeral Prefect server to start up before timing out.
            Defaults to 60.

    Yields:
        None: Control is yielded to the pytest execution environment while the
            isolated server remains alive. The server is cleanly shut down
            during session teardown.
    """
    os.environ["PREFECT_LOGGING_TO_API_WHEN_MISSING_FLOW"] = "ignore"

    with prefect_test_harness(server_startup_timeout=server_startup_timeout):
        yield
