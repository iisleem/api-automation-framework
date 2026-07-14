"""Starter service object for product catalog API tests."""

from __future__ import annotations

import httpx

from clients import ApiClient


class ProductCatalogService:
    def __init__(self, client: ApiClient) -> None:
        self.client = client

    def get_item(self, item_id: str) -> httpx.Response:
        return self.client.get(f"/catalog/items/{item_id}", expected_status=200)
