from __future__ import annotations

from pathlib import Path

from automation_core.reporting import get_or_install_allure_cli as core_get_or_install_allure_cli


def get_or_install_allure_cli(project_root: Path, logger) -> str | None:
    return core_get_or_install_allure_cli(project_root, logger=logger)
