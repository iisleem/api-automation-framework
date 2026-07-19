import automation_core
import pytest

pytestmark = pytest.mark.helpers


def test_automation_core_dependency_version():
    assert automation_core.__version__ == "0.10.1"
