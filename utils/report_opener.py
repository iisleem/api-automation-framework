from __future__ import annotations

from pathlib import Path

from automation_core.reporting import open_report as core_open_report


def open_report(report_path: Path, logger=None) -> bool:
    return core_open_report(report_path, logger=logger)
