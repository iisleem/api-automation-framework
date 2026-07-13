import pytest

from utils.helpers.soft_assertions import soft_assert

pytestmark = pytest.mark.helpers


def test_soft_assert_collects_grouped_failures():
    softly = soft_assert()

    softly.assert_equal("actual", "expected", "values should match")
    softly.assert_true(False, "condition should be true")

    with pytest.raises(AssertionError, match="Soft assertion failures"):
        softly.assert_all()


def test_soft_assert_passes_when_no_failures():
    softly = soft_assert()

    softly.assert_equal(1, 1)
    softly.assert_true(True, "condition should be true")
    softly.assert_all()
