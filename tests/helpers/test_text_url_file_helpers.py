from pathlib import Path

import pytest

from utils.helpers.files import assert_file_extension, assert_json_file_field, read_json_file
from utils.helpers.text import extract_first_match, extract_numbers, extract_otp, normalize_text
from utils.helpers.url import build_url, get_query_param, parse_query_params, remove_query_param

pytestmark = pytest.mark.helpers


def test_text_extractors_match_web_helper_style():
    assert normalize_text("Hello   API\nteam") == "Hello API team"
    assert extract_otp("Your code is 482913") == "482913"
    assert extract_first_match("Order ID: ORD-12345", r"Order ID: ([A-Z]+-\d+)") == "ORD-12345"
    assert extract_numbers("Total: 42. Tax: 3") == ["42", "3"]


def test_url_helpers_build_and_parse_query_strings():
    url = build_url("https://api.example.test", "users", {"page": 2, "tag": ["qa", "api"]})

    assert url == "https://api.example.test/users?page=2&tag=qa&tag=api"
    assert parse_query_params(url)["tag"] == ["qa", "api"]
    assert get_query_param(url, "page") == "2"
    assert remove_query_param(url, "page") == "https://api.example.test/users?tag=qa&tag=api"


def test_structured_file_helpers_validate_json(tmp_path: Path):
    payload_path = tmp_path / "payload.json"
    payload_path.write_text('{"user": {"name": "Ismail"}}', encoding="utf-8")

    assert read_json_file(payload_path)["user"]["name"] == "Ismail"
    assert_file_extension(payload_path, ".json")
    assert_json_file_field(payload_path, "user.name", "Ismail")
