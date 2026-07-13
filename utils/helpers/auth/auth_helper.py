"""Authentication helpers for API tests."""

from __future__ import annotations

import base64
import os
from dataclasses import dataclass, field
from typing import Protocol

SENSITIVE_HEADERS = {
    "authorization",
    "proxy-authorization",
    "x-api-key",
    "api-key",
    "cookie",
    "set-cookie",
}


class AuthProvider(Protocol):
    def headers(self) -> dict[str, str]:
        ...

    def params(self) -> dict[str, str]:
        ...


@dataclass(frozen=True)
class NoAuth:
    def headers(self) -> dict[str, str]:
        return {}

    def params(self) -> dict[str, str]:
        return {}


@dataclass(frozen=True)
class BearerTokenAuth:
    token: str

    def headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"}

    def params(self) -> dict[str, str]:
        return {}


@dataclass(frozen=True)
class BasicAuth:
    username: str
    password: str = field(repr=False)

    def headers(self) -> dict[str, str]:
        raw = f"{self.username}:{self.password}".encode("utf-8")
        return {"Authorization": f"Basic {base64.b64encode(raw).decode('ascii')}"}

    def params(self) -> dict[str, str]:
        return {}


@dataclass(frozen=True)
class ApiKeyAuth:
    key: str
    value: str = field(repr=False)
    location: str = "header"

    def headers(self) -> dict[str, str]:
        return {self.key: self.value} if self.location == "header" else {}

    def params(self) -> dict[str, str]:
        return {self.key: self.value} if self.location == "query" else {}


def build_auth_from_env(prefix: str = "API") -> AuthProvider:
    bearer_token = os.getenv(f"{prefix}_BEARER_TOKEN")
    if bearer_token:
        return BearerTokenAuth(bearer_token)

    api_key = os.getenv(f"{prefix}_KEY")
    api_key_name = os.getenv(f"{prefix}_KEY_NAME", "X-API-Key")
    if api_key:
        return ApiKeyAuth(api_key_name, api_key)

    username = os.getenv(f"{prefix}_USERNAME")
    password = os.getenv(f"{prefix}_PASSWORD")
    if username and password:
        return BasicAuth(username, password)

    return NoAuth()


def redact_headers(headers: dict[str, str], replacement: str = "***") -> dict[str, str]:
    return {
        key: replacement if key.lower() in SENSITIVE_HEADERS else value
        for key, value in headers.items()
    }
