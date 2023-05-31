from entest import depends_on
from .dependent_tests_C import mock_test_c1

@depends_on()
def mock_test_a1():
    print("running a1")

@depends_on(mock_test_c1)
def mock_test_a2():
    print("running a2")
    return {
        "value1":"Value 1"
    }

@depends_on()
def mock_test_a3():
    print("running a3")