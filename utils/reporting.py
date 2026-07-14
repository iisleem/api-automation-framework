from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

from automation_core.reporting import ReportingFinalizeResult, finalize_allure_reporting

ReportKind = str
REPORT_KIND_CHOICES = ("core", "summary", "allure", "both")

DEFAULT_RESULTS_DIR = Path("reports/allure-results")
DEFAULT_CORE_REPORT_DIR = Path("reports/automation-report")
DEFAULT_ALLURE_REPORT_DIR = Path("reports/allure-report")
DEFAULT_HISTORY_DIR = Path("reports/history")

PROJECT_NAME = "api-automation-framework"
FRAMEWORK_NAME = "pytest-api"
API_PROFILE = "REST/GraphQL/Contracts"
MATRIX_DIMENSIONS = ["environment", "profile", "api_profile", "domain"]


def finalize_api_reporting(
    project_root: Path,
    *,
    results_dir: Path | None = None,
    output_dir: Path | None = None,
    report_kind: ReportKind = "core",
    open_report: bool = False,
    env_name: str = "mock",
    base_url: str | None = None,
    graphql_url: str | None = None,
    run_id: str | None = None,
    history_dir: Path | None = None,
    allure_output_dir: Path | None = None,
    missing_ok: bool = False,
    install_allure_cli: bool = False,
    logger=None,
) -> ReportingFinalizeResult:
    metadata = build_api_report_metadata(
        env_name=env_name,
        base_url=base_url,
        graphql_url=graphql_url,
    )
    root = Path(project_root)
    return finalize_allure_reporting(
        results_dir or root / DEFAULT_RESULTS_DIR,
        output_dir or root / DEFAULT_CORE_REPORT_DIR,
        project_name=PROJECT_NAME,
        framework=FRAMEWORK_NAME,
        run_id=run_id,
        history_dir=history_dir if history_dir is not None else root / DEFAULT_HISTORY_DIR,
        open_report=open_report,
        report_kind=report_kind,
        missing_ok=missing_ok,
        allure_output_dir=allure_output_dir or root / DEFAULT_ALLURE_REPORT_DIR,
        metadata=metadata,
        enrichers=[api_metadata_enricher(metadata)],
        matrix_dimensions=MATRIX_DIMENSIONS,
        install_allure_cli=install_allure_cli,
        logger=None,
    )


def build_api_report_metadata(
    *,
    env_name: str = "mock",
    base_url: str | None = None,
    graphql_url: str | None = None,
) -> dict[str, str]:
    metadata = {
        "domain": "api",
        "profile": API_PROFILE,
        "api_profile": API_PROFILE,
        "environment": env_name or "mock",
    }
    if base_url:
        metadata["base_url"] = base_url
    if graphql_url:
        metadata["graphql_url"] = graphql_url
    return metadata


def api_metadata_enricher(metadata: dict[str, str]) -> Callable[[Any], Any]:
    def enrich(report: Any) -> Any:
        for test in getattr(report, "tests", []):
            test.domain = test.domain or metadata["domain"]
            test.profile = test.profile or metadata["profile"]
            test.environment = test.environment or metadata["environment"]
            test.metadata.setdefault("api_profile", metadata["api_profile"])
            if "base_url" in metadata:
                test.metadata.setdefault("base_url", metadata["base_url"])
            if "graphql_url" in metadata:
                test.metadata.setdefault("graphql_url", metadata["graphql_url"])
        return report

    return enrich


def generated_report_path(result: ReportingFinalizeResult) -> Path | None:
    for status in (result.core, result.summary, result.allure):
        if status.generated and status.path:
            return Path(status.path)
    return None


def log_reporting_result(result: ReportingFinalizeResult, logger=None) -> None:
    for label, status in (("Core", result.core), ("Summary", result.summary), ("Allure", result.allure)):
        if not status.requested:
            continue
        if status.generated:
            _log(logger, "info", "%s report generated: %s", label, status.path)
        else:
            detail = status.error or "; ".join(status.warnings) or status.status
            _log(logger, "warning", "%s report %s: %s", label, status.status, detail)

    for warning in result.warnings:
        _log(logger, "warning", "Reporting warning: %s", warning)
    for error in result.errors:
        _log(logger, "warning", "Reporting error: %s", error)
    if result.opened_path:
        level = "info" if result.opened else "warning"
        message = "Opened report: %s" if result.opened else "Could not open report: %s"
        _log(logger, level, message, result.opened_path)


def print_reporting_result(result: ReportingFinalizeResult) -> None:
    for label, status in (("Core", result.core), ("Summary", result.summary), ("Allure", result.allure)):
        if not status.requested:
            continue
        if status.generated:
            print(f"{label} report generated: {status.path}")
        else:
            detail = status.error or "; ".join(status.warnings) or status.status
            print(f"{label} report {status.status}: {detail}")

    for warning in result.warnings:
        print(f"Warning: {warning}")
    for error in result.errors:
        print(f"Error: {error}")
    if result.opened_path:
        print(f"Opened report: {result.opened_path}" if result.opened else f"Report not opened: {result.opened_path}")


def _log(logger, level: str, message: str, *args: object) -> None:
    if logger:
        getattr(logger, level)(message, *args)
