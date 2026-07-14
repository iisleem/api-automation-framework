import pytest

import framework

pytestmark = pytest.mark.helpers


def test_single_shortcut_marker_builds_marker_expression(monkeypatch):
    command = _build_run_command(monkeypatch, "--env", "mock", "--smoke")

    assert _marker_expression_from(command) == "smoke"


def test_multiple_shortcut_markers_build_union_expression(monkeypatch):
    command = _build_run_command(monkeypatch, "--env", "mock", "--smoke", "--contract")

    assert _marker_expression_from(command) == "smoke or contract"


def test_raw_marker_expression_is_respected(monkeypatch):
    command = _build_run_command(monkeypatch, "--env", "mock", "--markers", "smoke and not flaky")

    assert _marker_expression_from(command) == "smoke and not flaky"


def _build_run_command(monkeypatch: pytest.MonkeyPatch, *cli_args: str) -> list[str]:
    captured: dict[str, list[str]] = {}

    def fake_run_command(command: list[str]) -> int:
        captured["command"] = command
        return 0

    parser = framework._build_parser()
    args = parser.parse_args(["run", *cli_args])
    monkeypatch.setattr(framework, "_run_command", fake_run_command)

    assert framework._run_tests(args, []) == 0
    return captured["command"]


def _marker_expression_from(command: list[str]) -> str:
    marker_index = len(command) - 1 - command[::-1].index("-m")
    return command[marker_index + 1]
