import random
from collections import defaultdict
from sys import exit
from typing import List

try:
    from tests.conftest import Conftest as UserConftest
except ImportError:
    print(
        """
        You need to define conftest.py in your tests/ folder.
        The file should include a class Conftest that does not inherit anything.
        You can use super() to access the default method definitions.
        For example this is good enough:

# tests/conftest.py
class Conftest:
    pass

    """
    )
    exit(5)


class DefaultConftest:
    RANDOM_SEED = 1

    def __init__(self) -> None:
        random.seed(self.RANDOM_SEED)

    def get_testing_order(self, tests_to_be_run: List["TestCase"]):
        """
        Note that there is no requirement for the returned list to contain
        all elements of the one passed as the argument.
        """
        order = []
        unvisited = tests_to_be_run.copy()
        danger_zone = defaultdict(int)
        for test in filter(lambda test: test.without, unvisited):
            danger_zone[test.without] += 1
        while unvisited:
            random.shuffle(unvisited)
            start_len = len(unvisited)
            for test in unvisited:
                if all(parent in order for parent in test.parents) and danger_zone[test] <= 0:
                    order.append(test)
                    unvisited.remove(test)
                    danger_zone[test.without] -= 1
            if len(unvisited) == start_len:
                raise Exception(
                    "Impossible to traverse all graph nodes. Use --graph to review dependencies",
                )
        order.sort(key=lambda test_case: int(test_case.run_last))
        return order


class Conftest(UserConftest, DefaultConftest):
    pass


conftest = Conftest()
