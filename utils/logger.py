"""Framework logging setup."""

from __future__ import annotations

import logging
from pathlib import Path


def get_logger(name: str = "api-framework", log_file: str | Path | None = None) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    reports_dir = Path(__file__).resolve().parents[1] / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    path = Path(log_file) if log_file else reports_dir / "framework.log"
    path.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(path, mode="a", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
