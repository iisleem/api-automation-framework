from pathlib import Path

import pytest
import yaml

from utils.helpers.schema import SchemaValidator

pytestmark = pytest.mark.contract


def test_openapi_contract_loads_with_required_sections():
    contract = yaml.safe_load(Path("contracts/openapi/demo_booking_api.yaml").read_text(encoding="utf-8"))

    assert contract["openapi"].startswith("3.")
    assert "/health" in contract["paths"]
    assert "/bookings" in contract["paths"]
    assert "BookingResponse" in contract["components"]["schemas"]


def test_json_schema_files_are_valid_draft_2020_12():
    validator = SchemaValidator()
    schema_paths = sorted(Path("schemas").rglob("*.schema.json"))

    assert schema_paths
    for schema_path in schema_paths:
        assert validator.load_schema(schema_path)
