import httpx
import pytest
from services.product_catalog_service import ProductCatalogService

from clients import ApiClient

pytestmark = [pytest.mark.smoke, pytest.mark.rest]


def test_catalog_item_contract(schema_validator):
    client = ApiClient("https://product-api.example.test", transport=httpx.MockTransport(_catalog_handler))
    service = ProductCatalogService(client)

    response = service.get_item("SKU-1001")

    assert response.status_code == 200
    schema_validator.assert_matches_schema(response.json(), "schemas/rest/catalog_item.schema.json")
    client.close()


def _catalog_handler(request: httpx.Request) -> httpx.Response:
    if request.method == "GET" and request.url.path == "/catalog/items/SKU-1001":
        return httpx.Response(
            200,
            json={
                "id": "SKU-1001",
                "name": "Starter Item",
                "active": True,
                "price": 19.99,
            },
            headers={"content-type": "application/json"},
        )

    return httpx.Response(404, json={"error": "not found"})
