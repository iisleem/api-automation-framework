from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
_ENV_PATTERN = re.compile(r"\$\{([^}:]+)(?::-([^}]*))?\}")


class ConfigReader:
    def __init__(self, project_root: Path | None = None) -> None:
        self.project_root = project_root or PROJECT_ROOT
        self.config_dir = self.project_root / "config"

    def read_settings(self) -> dict[str, Any]:
        return _expand_env(self._read_yaml(self.config_dir / "settings.yaml"))

    def read_environments(self) -> dict[str, Any]:
        return _expand_env(self._read_yaml(self.config_dir / "environments.yaml"))

    def get_environment_config(self, env_name: str) -> dict[str, Any]:
        environments = self.read_environments()
        if env_name not in environments:
            available = ", ".join(sorted(environments))
            raise ValueError(f"Unknown environment '{env_name}'. Available: {available}")
        return environments[env_name]

    def load(self, env_name: str) -> dict[str, Any]:
        settings = self.read_settings()
        environment = self.get_environment_config(env_name)
        return {"env": env_name, **settings, **environment}

    @staticmethod
    def _read_yaml(path: Path) -> dict[str, Any]:
        with path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
        return data or {}


def resolve_path(path: str | Path) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else PROJECT_ROOT / candidate


def _expand_env_value(value: str) -> str:
    def replace(match: re.Match[str]) -> str:
        name = match.group(1)
        fallback = match.group(2) or ""
        return os.getenv(name, fallback)

    return _ENV_PATTERN.sub(replace, value)


def _expand_env(data: Any) -> Any:
    if isinstance(data, dict):
        return {key: _expand_env(value) for key, value in data.items()}
    if isinstance(data, list):
        return [_expand_env(item) for item in data]
    if isinstance(data, str):
        return _expand_env_value(data)
    return data


def load_yaml(path: str | Path) -> dict[str, Any]:
    with resolve_path(path).open(encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected YAML object in {path}")
    return _expand_env(data)


def load_json(path: str | Path) -> Any:
    with resolve_path(path).open(encoding="utf-8") as file:
        return json.load(file)


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


def deep_get(data: dict[str, Any], dotted_path: str, default: Any = None) -> Any:
    current: Any = data
    for part in dotted_path.split("."):
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current
