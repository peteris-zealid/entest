import importlib
from os import environ
from inspect import getfullargspec
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set

from entest.const import STATUS, display


class TestCase:
    full_registry: Dict[str, "TestCase"] = {}
    dynamic_globals: Dict[str, Any] = {}
    children: List["TestCase"]
    without: Optional["TestCase"]

    def __init__(self, func: Callable[[], None], parents: List["TestCase"], run_last=False):
        for parent in parents:
            #  if not isinstance(parent, TestCase):
            #      raise Exception("cannot depend on undecorated function")
            parent.children.append(self)
        self.func = func
        self.parents = list(parents)
        self.run_last = run_last
        self.children = []
        self.without = None
        self.status = STATUS.none
        if self.func.__name__ in self.full_registry:
            print("warning: a test with this name already exists")
        self.full_registry[self.func.__name__] = self
        if parents:
            self.depth: int = max((parent.depth for parent in parents)) + 1
        else:
            self.depth = 0
        self.error: Optional[Exception] = None

    def __call__(self) -> bool:
        if self.status == STATUS.none:
            raise Exception("Test is was not expected to run")
        if self.status != STATUS.wait:
            raise Exception("Test is being run more than once")
        if any((test.status in [STATUS.error, STATUS.deps_failed] for test in self.parents)):
            self.status = STATUS.deps_failed
            return False
        if any((test.status not in [STATUS.passed, STATUS.wip] for test in self.parents)):
            raise Exception(
                "Test is being run before its dependencies have finished running.", self
            )
        if self.without and self.without.status not in [STATUS.none, STATUS.wait]:
            raise Exception(
                f"Test ({self.without}) is not allowed to be run before this test.",
                "See 'without' flag for more info.",
                self,
            )
        self.status = STATUS.running
        required_globals = getfullargspec(self.func).args
        missing_globals = set(required_globals) - set(self.dynamic_globals.keys())
        if missing_globals:
            raise Exception("Cannot run test. Some globals are missing", missing_globals)
        try:
            new_globals = self.func(*[self.dynamic_globals[key] for key in required_globals])
        except Exception as err:
            self.status = STATUS.error
            self.error = err
            return False
        if new_globals:
            if new_globals == "wip":
                self.status = STATUS.wip
                return False
            if isinstance(new_globals, tuple) and new_globals[0] == "wip":
                self.status = STATUS.wip
                new_globals = new_globals[1]
            if not isinstance(new_globals, dict):
                raise Exception("return value from test case should be a dict")
            self.dynamic_globals.update(new_globals)
        self.status = STATUS.passed
        return True

    def name(self):
        return self.func.__name__

    def display(self):
        return f"{display(self.status):<11}|{' ' * self.depth}{self.name()}"

    def __str__(self):
        return self.name()

    def __repr__(self):
        return self.display()

    @classmethod
    def set_globals_dict(cls, d: dict):
        cls.dynamic_globals = d

    @classmethod
    def summary(cls, as_dict=False):
        report = {
            "total": len(cls.full_registry),
        }
        report.update(
            {
                status: len([None for t in cls.full_registry.values() if t.status == status])
                for status in STATUS
            }
        )
        if as_dict:
            return report
        else:
            return [
                f"""Total: {report['total']}""",
                f"""{display(STATUS.passed)}: {report[STATUS.passed]}""",
                f"""{display(STATUS.error)}: {report[STATUS.error]}""",
                f"""{display(STATUS.deps_failed)}: {report[STATUS.deps_failed]}""",
            ]

    @classmethod
    def error_summary(cls):
        return [
            f"""===== {test.name()} =====\n{test.error}\n"""
            for test in cls.full_registry.values()
            if test.error is not None
        ]


def empty_setup():
    pass


TEST_ROOT = TestCase(empty_setup, [])  ## make this singleton


def setup_setup(callback: Callable[[], None]) -> None:
    TEST_ROOT.func = callback


class DependsOn:
    LAST_DECORATED = TEST_ROOT

    def __init__(self):
        self.fixtures = {}

    def __call__(
        self, *requires: TestCase, previous: bool = None, without: TestCase = None, run_last=False
    ) -> Callable[[Callable], TestCase]:
        """
        For "previous" keyword to work as expected this decorator should be the last one applied.
        "run_last" is a temporary workaround to mark tests that delete important resources.
        "without" is used to mark a single test as a must NOT have dependency
        """
        if previous is None:
            previous = len(requires) == 0

        def decorator(func):
            parents = list(requires)
            if previous:
                parents.append(DependsOn.LAST_DECORATED)
            test_case = TestCase(func, parents, run_last=run_last)
            if without:
                test_case.without = without
            DependsOn.LAST_DECORATED = test_case
            return test_case

        return decorator


depends_on = DependsOn()


def remove_implicit_edges(dfs_path: List[TestCase], logger=print):
    head = dfs_path[-1]
    for child in head.children:
        for parent in dfs_path[:-1]:
            if child in parent.children:
                logger("Warning: Transitive node detected. From", parent.name(), "to", child.name())
                parent.children.remove(child)
                child.parents.remove(parent)
        dfs_path.append(child)
        remove_implicit_edges(dfs_path)
    dfs_path.pop()


def propogate_status_none() -> int:
    unvisited = {tc for tc in TestCase.full_registry.values() if tc.status == STATUS.wait}
    number_of_tests_to_run = len(unvisited)
    while unvisited:
        new_unvisited = set()
        for test_case in unvisited:
            number_of_tests_to_run += int(test_case.status != STATUS.wait)
            test_case.status = STATUS.wait
            new_unvisited.update(test_case.parents)
        unvisited = new_unvisited
    return number_of_tests_to_run


def test_discovery(dirs: List[Path], logger=print):
    logger('Collecting tests')
    if TEST_ROOT.children:
        raise Exception("do not run test_discovery twice")
    paths = list(Path('tests').glob("**/*.py"))
    shortlist: List[Path] = []
    if dirs:
        for dir in dirs:
            shortlist.extend(dir.glob("**/*.py") if dir.is_dir() else [dir])
    else:
        shortlist = paths
    for path in paths:
        file_contents = path.read_bytes()
        if b"from entest" in file_contents or b"import entest" in file_contents:
            DependsOn.LAST_DECORATED = TEST_ROOT
            lib = importlib.import_module(str(path).replace("/", ".")[:-3])
            if path in shortlist:
                for var in lib.__dict__.values():
                    if isinstance(var, TestCase):
                        var.status = STATUS.wait
                        if environ.get("ENTEST_SKIP_TEARDOWN", False) and var.run_last:
                            var.status = STATUS.none
    logger(f'Collected {len(TestCase.full_registry)} tests')
    logger('Removing implicit edges')
    remove_implicit_edges([TEST_ROOT], logger)
    logger('Resolving dependencies')
    number_of_tests_to_run = propogate_status_none()
    logger(f'Will run {number_of_tests_to_run} tests')
