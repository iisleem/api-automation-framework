"""Framework logging setup."""

from __future__ import annotations

import logging
from pathlib import Path

from automation_core.logger import get_logger as core_get_logger

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def get_logger(name: str = "api-framework", log_file: str | Path | None = None) -> logging.Logger:
    path = Path(log_file) if log_file else PROJECT_ROOT / "reports" / "framework.log"
    return core_get_logger(name, level=logging.INFO, log_file=path)
