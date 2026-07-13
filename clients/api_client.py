"""HTTP client wrapper for REST API tests."""

from __future__ import annotations

import json
import uuid
from collections.abc import Mapping
from typing import Any

import httpx

from utils.helpers.assertions import assert_status
from utils.helpers.auth import NoAuth, redact_headers
from utils.helpers.auth.auth_helper import AuthProvider

try:
    import allure
except Exception:  # pragma: no cover - only used when allure is absent locally
    allure = None


class ApiClient:
    def __init__(
        self,
        base_url: str,
        *,
        default_headers: Mapping[str, str] | None = None,
        timeout: float = 15,
        auth: AuthProvider | None = None,
        verify_ssl: bool = True,
        follow_redirects: bool = True,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/") if base_url else ""
        self.default_headers = dict(default_headers or {})
        self.auth = auth or NoAuth()
        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
            verify=verify_ssl,
            follow_redirects=follow_redirects,
            transport=transport,
        )

    def close(self) -> None:
        self.client.close()

    def __enter__(self) -> "ApiClient":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json_body: Any | None = None,
        data: Any | None = None,
        headers: Mapping[str, str] | None = None,
        expected_status: int | list[int] | tuple[int, ...] | None = None,
        **kwargs: Any,
    ) -> httpx.Response:
        request_headers = self._merge_headers(headers)
        request_params = self._merge_params(params)
        response = self.client.request(
            method=method.upper(),
            url=path,
            params=request_params,
            json=json_body,
            data=data,
            headers=request_headers,
            **kwargs,
        )
        self._attach_exchange(method, path, request_headers, request_params, json_body, response)
        if expected_status is not None:
            assert_status(response, expected_status)
        return response

    def get(self, path: str, **kwargs: Any) -> httpx.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> httpx.Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> httpx.Response:
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> httpx.Response:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> httpx.Response:
        return self.request("DELETE", path, **kwargs)

    def _merge_headers(self, headers: Mapping[str, str] | None) -> dict[str, str]:
        merged = dict(self.default_headers)
        merged.update(self.auth.headers())
        merged.update(headers or {})
        merged.setdefault("X-Request-ID", f"api-fw-{uuid.uuid4().hex}")
        return merged

    def _merge_params(self, params: Mapping[str, Any] | None) -> dict[str, Any]:
        merged = dict(params or {})
        merged.update(self.auth.params())
        return merged

    def _attach_exchange(
        self,
        method: str,
        path: str,
        headers: Mapping[str, str],
        params: Mapping[str, Any],
        request_body: Any,
        response: httpx.Response,
    ) -> None:
        if allure is None:
            return
        payload = {
            "request": {
                "method": method.upper(),
                "url": str(response.request.url),
                "path": path,
                "params": dict(params),
                "headers": redact_headers(dict(headers)),
                "body": request_body,
            },
            "response": {
                "status_code": response.status_code,
                "headers": redact_headers(dict(response.headers)),
                "body": _safe_response_body(response),
            },
        }
        allure.attach(
            json.dumps(payload, indent=2, default=str),
            name=f"{method.upper()} {path}",
            attachment_type=allure.attachment_type.JSON,
        )


def _safe_response_body(response: httpx.Response) -> Any:
    content_type = response.headers.get("content-type", "")
    if "application/json" in content_type:
        try:
            return response.json()
        except ValueError:
            return response.text
    return response.text[:2000]
