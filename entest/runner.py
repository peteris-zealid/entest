from typing import Callable

from entest.const import STATUS
from entest.dependency_decorator import TEST_ROOT, TestCase


def breadth_first_traverse(root: TestCase):
    order = []
    nodes = [root]
    current_depth = 0
    while nodes:
        order.extend(nodes)
        current_depth += 1
        nodes = [test for test in TestCase.full_registry.values() if test.depth == current_depth]
    order.sort(key=lambda test_case: int(test_case.run_last))
    return order


def generate_run_sequence(*, root=TEST_ROOT, strategy=breadth_first_traverse):
    order = strategy(root)
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
