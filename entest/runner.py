from typing import Callable
import random

from entest.const import STATUS
from entest.dependency_decorator import TEST_ROOT, TestCase


def breadth_first_traverse(root: TestCase=TEST_ROOT):
    order = []
    nodes = [root]
    current_depth = 0
    while nodes:
        order.extend(nodes)
        current_depth += 1
        nodes = [test for test in TestCase.full_registry.values() if test.depth == current_depth]
    order.sort(key=lambda test_case: int(test_case.run_last))
    return order

def bogo_order(seed: int=0):
    random.seed(seed)
    order = []
    unvisited = [test for test in TestCase.full_registry.values()]
    while unvisited:
        random.shuffle(unvisited)
        for test in unvisited:
            if all(parent in order for parent in test.parents):
                order.append(test)
                unvisited.remove(test)
    return order

def generate_run_sequence(*, strategy=bogo_order):
    order = strategy()
    return [tc for tc in order if tc.status == STATUS.wait]


def run_tests(logger: Callable[..., None]):
    logger("""=============== Running tests ===============""")
    for test in generate_run_sequence():
        test()
        logger(test.display())
    logger("""=================== ERRORS ==================""")
    logger("\n".join(TestCase.error_summary()))
    logger("""================== Summary ==================""")
    logger("\n".join(TestCase.summary()))
