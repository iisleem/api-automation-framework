"""GraphQL client wrapper."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import httpx

from clients.api_client import ApiClient


class GraphQLClient:
    def __init__(
        self, base_url: str, *, endpoint: str = "", api_client: ApiClient | None = None, **kwargs: Any
    ) -> None:
        self.endpoint = endpoint
        self.api_client = api_client or ApiClient(base_url, **kwargs)

    def close(self) -> None:
        self.api_client.close()

    def execute(
        self,
        query: str,
        *,
        variables: dict[str, Any] | None = None,
        operation_name: str | None = None,
        expected_status: int = 200,
    ) -> httpx.Response:
        payload: dict[str, Any] = {"query": query}
        if variables is not None:
            payload["variables"] = variables
        if operation_name:
            payload["operationName"] = operation_name
        return self.api_client.post(self.endpoint, json_body=payload, expected_status=expected_status)

    def execute_file(
        self,
        query_path: str | Path,
        *,
        variables: dict[str, Any] | None = None,
        operation_name: str | None = None,
        expected_status: int = 200,
    ) -> httpx.Response:
        query = Path(query_path).read_text(encoding="utf-8")
        return self.execute(
            query,
            variables=variables,
            operation_name=operation_name,
            expected_status=expected_status,
        )

    @staticmethod
    def assert_no_errors(payload: dict[str, Any]) -> None:
        assert not payload.get("errors"), f"GraphQL returned errors: {payload.get('errors')}"
