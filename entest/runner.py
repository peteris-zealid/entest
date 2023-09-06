import threading
from os import abort
from typing import Callable

from entest.conftest import conftest
from entest.const import STATUS
from entest.dependency_decorator import TEST_ROOT, TestCase
from entest.status_report import IS_STACKPRINTER, StatusPanel


def run_tests(logger: Callable[..., None]):
    logger("""=============== Running tests ===============""")
    tests_to_be_run = [tc for tc in TestCase.full_registry.values() if tc.status == STATUS.wait]
    test_order = conftest.get_testing_order(tests_to_be_run)
    # TODO check test_order is valid (because ordering can be defined by user)
    with StatusPanel(test_order, logger):
        for test in test_order:
            test()
    logger("""=================== ERRORS ==================""")
    # It is an ugly hack to use IS_STACKPRINTER here but logging should be refactored in general
    TestCase.print_error_summary(logger if not IS_STACKPRINTER else print)
    join_dangling_threads(logger)
    logger("""================== Summary ==================""")
    logger("\n".join(TestCase.summary()))


def join_dangling_threads(logger: Callable[..., None]) -> None:
    thread_count = threading.active_count() - 1
    if thread_count == 0:
        return
    logger(f"Found {thread_count} dangling threads.")
    for thread in threading.enumerate():
        if thread is threading.current_thread():
            continue
        else:
            thread.join(timeout=10)
            if thread.is_alive:
                logger("Some non-daemon threads could not be joined.", flush=True)
                abort()
