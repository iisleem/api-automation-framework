import pytest

from utils.helpers.cleanup import CleanupRegistry, assert_cleanup_success

pytestmark = pytest.mark.helpers


def test_cleanup_registry_runs_actions_lifo():
    calls = []
    cleanup = CleanupRegistry()
    cleanup.add("first", calls.append, "first")
    cleanup.add("second", calls.append, "second")

    results = cleanup.run_all()

    assert calls == ["second", "first"]
    assert_cleanup_success(results)
    assert cleanup.actions == ()


def test_cleanup_registry_reports_failures():
    cleanup = CleanupRegistry()
    cleanup.add("broken cleanup", _raise_runtime_error)

    results = cleanup.run_all()

    with pytest.raises(AssertionError, match="Cleanup actions failed"):
        assert_cleanup_success(results)


def _raise_runtime_error():
    raise RuntimeError("boom")
