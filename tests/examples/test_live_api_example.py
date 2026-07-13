import pytest


@pytest.mark.live
@pytest.mark.rest
def test_live_health_endpoint_example(api_client, schema_validator):
    response = api_client.get("/health", expected_status=200)

    schema_validator.assert_matches_schema(response.json(), "schemas/rest/health.schema.json")
