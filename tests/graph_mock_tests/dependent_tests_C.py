from entest import depends_on

@depends_on()
def mock_test_c1():
    print("running c1")
