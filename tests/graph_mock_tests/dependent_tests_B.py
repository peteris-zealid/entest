from entest import depends_on
from .dependent_tests_A import mock_test_a2

@depends_on(mock_test_a2)
def mock_test_b2(value1):
    print("running b2")
    assert value1 == "Value 1"