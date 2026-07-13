"""JSON Schema validation helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError

from utils.config_reader import resolve_path


class SchemaValidator:
    def __init__(self) -> None:
        self._format_checker = FormatChecker()

    def load_schema(self, schema_path: str | Path) -> dict[str, Any]:
        with resolve_path(schema_path).open(encoding="utf-8") as file:
            schema = json.load(file)
        Draft202012Validator.check_schema(schema)
        return schema

    def validate(self, payload: Any, schema: dict[str, Any] | str | Path) -> None:
        resolved_schema = self.load_schema(schema) if isinstance(schema, (str, Path)) else schema
        validator = Draft202012Validator(resolved_schema, format_checker=self._format_checker)
        errors = sorted(validator.iter_errors(payload), key=lambda error: list(error.path))
        if errors:
            raise self._format_error(errors[0])

    def assert_matches_schema(self, payload: Any, schema: dict[str, Any] | str | Path) -> None:
        self.validate(payload, schema)

    @staticmethod
    def _format_error(error: ValidationError) -> AssertionError:
        location = ".".join(str(part) for part in error.path) or "<root>"
        return AssertionError(f"Schema validation failed at {location}: {error.message}")
