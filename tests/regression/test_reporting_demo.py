import pytest

from utils.assertions import assert_equal


@pytest.mark.regression
@pytest.mark.reporting_demo
def test_intentional_failure_generates_api_artifacts():
    assert_equal(
        200,
        500,
        "Intentional failure: API status is expected to be wrong",
    )
