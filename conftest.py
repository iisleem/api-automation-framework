from __future__ import annotations

import os
import subprocess
from collections.abc import Iterator
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

import pytest
from dotenv import load_dotenv

from clients import ApiClient, GraphQLClient
from utils.allure_cli import get_or_install_allure_cli
from utils.config_reader import ConfigReader
from utils.data_reader import DataReader
from utils.helpers.auth import build_auth_from_env
from utils.helpers.schema import SchemaValidator
from utils.logger import get_logger
from utils.report_generator import generate_html_report
from utils.report_opener import open_report

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent
LOGGER = get_logger("framework")
ARTIFACT_DIRECTORIES = ("reports", "logs")


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("api-automation-framework")
    group.addoption(
        "--env",
        action="store",
        default="mock",
        help="Environment name from config/environments.yaml. Example: --env qa",
    )
    group.addoption(
        "--base-url",
        action="store",
        default=None,
        help="Override REST API base URL.",
    )
    group.addoption(
        "--graphql-url",
        action="store",
        default=None,
        help="Override GraphQL endpoint URL.",
    )
    group.addoption(
        "--api-timeout",
        action="store",
        default=None,
        type=float,
        help="Override API timeout in seconds.",
    )
    group.addoption(
        "--enable-live-api-examples",
        action="store_true",
        default=False,
        help="Run opt-in tests marked live.",
    )
    group.addoption(
        "--run-reporting-demo",
        action="store_true",
        default=False,
        help="Include the intentionally failing reporting demo test.",
    )
    group.addoption(
        "--no-generate-report",
        action="store_true",
        default=False,
        help="Do not generate the HTML report after the test session.",
    )
    group.addoption(
        "--no-open-report",
        action="store_true",
        default=False,
        help="Do not open the generated HTML report in the default browser.",
    )


def pytest_configure() -> None:
    for directory in ARTIFACT_DIRECTORIES:
        (PROJECT_ROOT / directory).mkdir(parents=True, exist_ok=True)


def pytest_collection_modifyitems(
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    if not _live_enabled(config):
        skip_live = pytest.mark.skip(
            reason="Live API examples are disabled. Use --enable-live-api-examples to include them."
        )
        for item in items:
            if "live" in item.keywords:
                item.add_marker(skip_live)

    if config.getoption("--run-reporting-demo"):
        return

    skip_reporting_demo = pytest.mark.skip(
        reason="Intentional reporting demo. Run with --run-reporting-demo to include it."
    )
    for item in items:
        if "reporting_demo" in item.keywords:
            item.add_marker(skip_reporting_demo)


def pytest_sessionfinish(
    session: pytest.Session,
    exitstatus: int,
) -> None:
    if hasattr(session.config, "workerinput"):
        return
    if session.config.getoption("--no-generate-report"):
        return

    report_path = _generate_report_after_session()
    if report_path and not session.config.getoption("--no-open-report"):
        open_report(report_path, LOGGER)


@pytest.fixture(scope="session")
def framework_config(pytestconfig: pytest.Config) -> dict[str, Any]:
    env_name = pytestconfig.getoption("--env")
    config = ConfigReader(PROJECT_ROOT).load(env_name)
    if pytestconfig.getoption("--base-url"):
        config["base_url"] = pytestconfig.getoption("--base-url")
    if pytestconfig.getoption("--graphql-url"):
        config["graphql_url"] = pytestconfig.getoption("--graphql-url")
    LOGGER.info("Loaded framework config for environment: %s", env_name)
    return config


@pytest.fixture(scope="session")
def base_url(framework_config: dict[str, Any]) -> str:
    return framework_config["base_url"]


@pytest.fixture(scope="session")
def graphql_url(framework_config: dict[str, Any]) -> str:
    return framework_config["graphql_url"]


@pytest.fixture(scope="session")
def api_client(framework_config: dict[str, Any], pytestconfig: pytest.Config) -> Iterator[ApiClient]:
    timeout = pytestconfig.getoption("--api-timeout") or framework_config["timeouts"]["request_timeout_seconds"]
    client = ApiClient(
        framework_config["base_url"],
        default_headers=framework_config["api"]["default_headers"],
        timeout=timeout,
        verify_ssl=framework_config["api"]["verify_ssl"],
        follow_redirects=framework_config["api"]["follow_redirects"],
        auth=build_auth_from_env(),
    )
    yield client
    client.close()


@pytest.fixture(scope="session")
def graphql_client(
    framework_config: dict[str, Any],
    pytestconfig: pytest.Config,
) -> Iterator[GraphQLClient]:
    timeout = pytestconfig.getoption("--api-timeout") or framework_config["timeouts"]["request_timeout_seconds"]
    graphql_base_url, graphql_endpoint = _split_graphql_url(framework_config["graphql_url"])
    client = GraphQLClient(
        graphql_base_url,
        endpoint=graphql_endpoint,
        default_headers=framework_config["api"]["default_headers"],
        timeout=timeout,
        verify_ssl=framework_config["api"]["verify_ssl"],
        follow_redirects=framework_config["api"]["follow_redirects"],
        auth=build_auth_from_env(),
    )
    yield client
    client.close()


@pytest.fixture(scope="session")
def schema_validator() -> SchemaValidator:
    return SchemaValidator()


@pytest.fixture(scope="session")
def data_reader() -> DataReader:
    return DataReader(PROJECT_ROOT)


@pytest.fixture(scope="session")
def users(data_reader: DataReader) -> dict[str, Any]:
    return data_reader.read_json("users.json")


@pytest.fixture()
def booking_payload(data_reader: DataReader) -> dict[str, Any]:
    return data_reader.read_json("payloads/create_booking.json")


def _live_enabled(config: pytest.Config) -> bool:
    return config.getoption("--enable-live-api-examples") or os.getenv("ENABLE_LIVE_API_EXAMPLES") == "true"


def _split_graphql_url(graphql_url: str) -> tuple[str, str]:
    parsed = urlsplit(graphql_url)
    if not parsed.scheme or not parsed.netloc:
        return graphql_url, ""
    base_url = urlunsplit((parsed.scheme, parsed.netloc, "", "", ""))
    endpoint = parsed.path or "/graphql"
    if parsed.query:
        endpoint = f"{endpoint}?{parsed.query}"
    return base_url, endpoint


def _generate_report_after_session() -> Path | None:
    results_dir = PROJECT_ROOT / "reports" / "allure-results"
    output_dir = PROJECT_ROOT / "reports" / "allure-report"
    allure_executable = get_or_install_allure_cli(PROJECT_ROOT, LOGGER)

    try:
        if allure_executable:
            subprocess.run(
                [
                    allure_executable,
                    "generate",
                    str(results_dir),
                    "-o",
                    str(output_dir),
                    "--clean",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            report_path = output_dir / "index.html"
            LOGGER.info("Generated Allure report: %s", report_path)
            return report_path

        report_path = generate_html_report(results_dir, output_dir)
        LOGGER.info("Generated built-in HTML report: %s", report_path)
        return report_path
    except Exception as error:
        LOGGER.warning("Could not generate HTML report after test session: %s", error)
        return None
