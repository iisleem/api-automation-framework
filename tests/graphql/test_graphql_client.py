import json

import httpx
import pytest

from clients import GraphQLClient
from services import CountryService


@pytest.mark.graphql
@pytest.mark.smoke
def test_graphql_client_executes_query_and_matches_schema(schema_validator):
    client = GraphQLClient(
        "https://mock.api.local",
        endpoint="/graphql",
        transport=httpx.MockTransport(_graphql_handler),
    )
    service = CountryService(client)

    response = service.country_by_code("JO")
    payload = response.json()

    client.assert_no_errors(payload)
    assert payload["data"]["country"]["name"] == "Jordan"
    schema_validator.assert_matches_schema(payload, "schemas/graphql/country_response.schema.json")
    client.close()


def _graphql_handler(request: httpx.Request) -> httpx.Response:
    body = json.loads(request.content.decode("utf-8"))
    assert "CountryByCode" in body["query"]
    assert body["variables"] == {"code": "JO"}
    return httpx.Response(
        200,
        json={
            "data": {
                "country": {
                    "code": "JO",
                    "name": "Jordan",
                    "emoji": "JO",
                    "currency": "JOD",
                }
            }
        },
        headers={"content-type": "application/json"},
    )
