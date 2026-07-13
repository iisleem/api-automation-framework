"""Optional requests-based client for teams that prefer requests.Session."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any
from urllib.parse import urljoin

import requests

from utils.helpers.auth import NoAuth, redact_headers
from utils.helpers.auth.auth_helper import AuthProvider


class RequestsApiClient:
    def __init__(
        self,
        base_url: str,
        *,
        default_headers: Mapping[str, str] | None = None,
        timeout: float = 15,
        auth: AuthProvider | None = None,
        verify_ssl: bool = True,
        session: requests.Session | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/") + "/"
        self.default_headers = dict(default_headers or {})
        self.timeout = timeout
        self.auth = auth or NoAuth()
        self.verify_ssl = verify_ssl
        self.session = session or requests.Session()

    def close(self) -> None:
        self.session.close()

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
    ) -> requests.Response:
        request_headers = self._merge_headers(headers)
        request_params = dict(params or {})
        request_params.update(self.auth.params())
        response = self.session.request(
            method=method.upper(),
            url=urljoin(self.base_url, path.lstrip("/")),
            params=request_params,
            json=json_body,
            data=data,
            headers=request_headers,
            timeout=self.timeout,
            verify=self.verify_ssl,
            **kwargs,
        )
        if expected_status is not None:
            expected = [expected_status] if isinstance(expected_status, int) else list(expected_status)
            assert response.status_code in expected, (
                f"Expected status {expected}, got {response.status_code}. "
                f"Headers: {redact_headers(dict(response.headers))}. Body: {response.text[:500]}"
            )
        return response

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("DELETE", path, **kwargs)

    def _merge_headers(self, headers: Mapping[str, str] | None) -> dict[str, str]:
        merged = dict(self.default_headers)
        merged.update(self.auth.headers())
        merged.update(headers or {})
        return merged
