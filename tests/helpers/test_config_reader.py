import pytest

from utils.config_reader import deep_get, get_environment_config, load_environments, load_settings

pytestmark = pytest.mark.helpers


def test_load_settings_and_environments():
    settings = load_settings()
    environments = load_environments()

    assert settings["framework"]["name"] == "API Automation Framework"
    assert "mock" in environments


def test_environment_config_includes_selected_name():
    config = get_environment_config("mock")

    assert config["name"] == "mock"
    assert config["base_url"] == "https://mock.api.local"


def test_deep_get_returns_nested_values_and_default():
    payload = {"api": {"timeout": 15}}

    assert deep_get(payload, "api.timeout") == 15
    assert deep_get(payload, "api.missing", default="fallback") == "fallback"
