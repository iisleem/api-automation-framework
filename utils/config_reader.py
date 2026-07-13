from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from automation_core.config import ConfigReader as CoreConfigReader
from automation_core.config import deep_get
from automation_core.config import load_json as core_load_json
from automation_core.config import load_yaml as core_load_yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class ConfigReader(CoreConfigReader):
    def __init__(self, project_root: Path | None = None) -> None:
        super().__init__(project_root or PROJECT_ROOT)

    def load(self, env_name: str) -> dict[str, Any]:
        return super().load(env_name, environment_key="env", merge_environment=True)


def resolve_path(path: str | Path) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else PROJECT_ROOT / candidate


def load_yaml(path: str | Path) -> dict[str, Any]:
    data = core_load_yaml(resolve_path(path), base_dir=PROJECT_ROOT)
    if not isinstance(data, dict):
        raise ValueError(f"Expected YAML object in {path}")
    return data


def load_json(path: str | Path) -> Any:
    return core_load_json(resolve_path(path), base_dir=PROJECT_ROOT)


def load_settings() -> dict[str, Any]:
    return ConfigReader(PROJECT_ROOT).read_settings()


def load_environments() -> dict[str, Any]:
    return ConfigReader(PROJECT_ROOT).read_environments()


def get_environment_config(env: str | None = None) -> dict[str, Any]:
    settings = ConfigReader(PROJECT_ROOT).read_settings()
    env_name = env or os.getenv("API_ENV") or settings["framework"]["default_env"]
    config = dict(ConfigReader(PROJECT_ROOT).get_environment_config(env_name))
    config["name"] = env_name
    return config


__all__ = [
    "ConfigReader",
    "deep_get",
    "get_environment_config",
    "load_environments",
    "load_json",
    "load_settings",
    "load_yaml",
    "resolve_path",
]
