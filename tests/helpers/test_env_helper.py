import pytest

from utils.helpers.env import mask_secret, optional_env, require_env, validate_required_envs

pytestmark = pytest.mark.helpers


def test_env_helpers_read_required_optional_and_masked_values(monkeypatch):
    monkeypatch.setenv("API_TEST_SECRET", "secret-value")

    assert require_env("API_TEST_SECRET") == "secret-value"
    assert optional_env("MISSING_ENV", "fallback") == "fallback"
    assert validate_required_envs(["API_TEST_SECRET"]) == {"API_TEST_SECRET": "secret-value"}
    assert mask_secret("secret-value", visible_chars=5) == "*******value"


def test_require_env_reports_missing_value(monkeypatch):
    monkeypatch.delenv("API_TEST_SECRET", raising=False)

    with pytest.raises(EnvironmentError, match="Required environment variable"):
        require_env("API_TEST_SECRET")
