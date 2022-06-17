from typing import Callable
from collections import defaultdict
import random
import threading

from entest.const import STATUS
from entest.dependency_decorator import TEST_ROOT, TestCase
from entest.status_report import panel


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

def generate_run_sequence(*, strategy=bogo_order):
    order = strategy()
    return [tc for tc in order if tc.status == STATUS.wait]


def run_tests(logger: Callable[..., None]):
    logger("""=============== Running tests ===============""")
    test_order = generate_run_sequence()
    thread = threading.Thread(target=panel, args=(test_order, logger))
    thread.start()
    for test in test_order:
        test()
    thread.join(timeout=1)
    logger("""=================== ERRORS ==================""")
    logger("\n".join(TestCase.error_summary()))
    logger("""================== Summary ==================""")
    logger("\n".join(TestCase.summary()))
