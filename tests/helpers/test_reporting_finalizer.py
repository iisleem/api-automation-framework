import json
from types import SimpleNamespace

import pytest

import conftest as api_conftest
import framework
from utils.report_generator import finalize_allure_reporting
from utils.reporting import API_PROFILE, finalize_api_reporting

pytestmark = pytest.mark.helpers


def test_api_reporting_finalizer_generates_core_report_with_metadata(tmp_path):
    results_dir = _write_allure_result(tmp_path)

    result = finalize_api_reporting(
        tmp_path,
        results_dir=results_dir,
        output_dir=tmp_path / "automation-report",
        report_kind="core",
        env_name="mock",
        base_url="https://mock.api.local",
        graphql_url="https://mock.api.local/graphql",
        history_dir=tmp_path / "history",
    )

    report_path = tmp_path / "automation-report" / "index.html"
    report_data_path = tmp_path / "automation-report" / "report-data.json"
    run_report_path = tmp_path / "automation-report" / "data" / "run-report.json"
    run_report = json.loads(run_report_path.read_text(encoding="utf-8"))
    report_data = json.loads(report_data_path.read_text(encoding="utf-8"))

    assert result.ok is True
    assert result.core.generated is True
    assert report_path.exists()
    assert report_data_path.exists()
    assert run_report["metadata"]["domain"] == "api"
    assert run_report["metadata"]["api_profile"] == API_PROFILE
    assert run_report["metadata"]["environment"] == "mock"
    assert run_report["tests"][0]["domain"] == "api"
    assert run_report["tests"][0]["profile"] == API_PROFILE
    assert run_report["tests"][0]["environment"] == "mock"
    assert run_report["tests"][0]["metadata"]["api_profile"] == API_PROFILE
    assert report_data["run"]["summary"]["total"] == 1
    assert report_data["run"]["summary"]["status"] == "passed"
    assert report_data["timeline"]["event_counts"]["artifact"] == 1
    assert report_data["signals"]["artifact_count"] == 1


def test_api_reporting_both_keeps_core_when_official_allure_cli_is_missing(tmp_path, monkeypatch):
    results_dir = _write_allure_result(tmp_path)
    monkeypatch.setattr("automation_core.reporting.finalizer.get_allure_cli", lambda logger=None: None)

    result = finalize_api_reporting(
        tmp_path,
        results_dir=results_dir,
        output_dir=tmp_path / "automation-report",
        report_kind="both",
        env_name="mock",
        history_dir=tmp_path / "history",
    )

    assert result.ok is True
    assert result.core.generated is True
    assert result.allure.requested is True
    assert result.allure.status == "missing_cli"
    assert any("Allure CLI" in warning for warning in result.warnings)


def test_framework_cli_report_kind_options_default_to_core():
    parser = framework._build_parser()

    run_args = parser.parse_args(["run"])
    report_args = parser.parse_args(["report", "generate"])
    both_args = parser.parse_args(["run", "--report-kind", "both", "--install-allure-cli"])

    assert run_args.report_kind == "core"
    assert report_args.report_kind == "core"
    assert report_args.output == "reports/automation-report"
    assert both_args.report_kind == "both"
    assert both_args.install_allure_cli is True


def test_pytest_session_reporting_passes_selected_options(monkeypatch):
    captured = {}
    expected_result = SimpleNamespace(ok=True)

    def fake_finalize(project_root, **kwargs):
        captured["project_root"] = project_root
        captured.update(kwargs)
        return expected_result

    monkeypatch.setattr(api_conftest, "finalize_api_reporting", fake_finalize)

    result = api_conftest._generate_report_after_session(
        report_kind="both",
        open_report=False,
        env_name="mock",
        base_url="https://mock.api.local",
        graphql_url="https://mock.api.local/graphql",
        install_allure_cli=True,
    )

    assert result is expected_result
    assert captured["report_kind"] == "both"
    assert captured["open_report"] is False
    assert captured["env_name"] == "mock"
    assert captured["base_url"] == "https://mock.api.local"
    assert captured["graphql_url"] == "https://mock.api.local/graphql"
    assert captured["install_allure_cli"] is True
    assert captured["missing_ok"] is True


def test_report_generator_compatibility_wrapper_exports_core_finalizer():
    assert callable(finalize_allure_reporting)


def _write_allure_result(tmp_path):
    results_dir = tmp_path / "allure-results"
    results_dir.mkdir()
    (results_dir / "api-case-result.json").write_text(
        json.dumps(
            {
                "historyId": "api-case",
                "name": "test_api_case",
                "fullName": "tests.smoke.test_api_case",
                "status": "passed",
                "start": 100,
                "stop": 250,
                "attachments": [
                    {
                        "name": "GET /health response",
                        "source": "response.json",
                        "type": "application/json",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    (results_dir / "response.json").write_text(
        json.dumps({"request": {"method": "GET"}, "response": {"status_code": 200}}),
        encoding="utf-8",
    )
    return results_dir
