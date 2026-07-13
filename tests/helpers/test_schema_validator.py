import pytest

from utils.helpers.schema import SchemaValidator

pytestmark = pytest.mark.helpers


def test_schema_validator_accepts_valid_payload():
    validator = SchemaValidator()
    payload = {
        "status": "ok",
        "service": "booking-api",
        "timestamp": "2026-07-13T09:00:00Z",
    }

    validator.assert_matches_schema(payload, "schemas/rest/health.schema.json")


def test_schema_validator_raises_readable_error_for_invalid_payload():
    validator = SchemaValidator()
    payload = {"status": "missing-fields"}

    with pytest.raises(AssertionError, match="Schema validation failed"):
        validator.assert_matches_schema(payload, "schemas/rest/health.schema.json")
