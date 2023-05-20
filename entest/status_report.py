import threading
import time
from sys import stderr
from traceback import format_tb

try:
    from rich.console import Console
    from rich.live import Live
    from rich.table import Table
    from rich.traceback import Traceback

    IS_RICH = True
except ImportError:
    IS_RICH = False
    Table = None

try:
    import stackprinter

    IS_STACKPRINTER = True
except ImportError:
    stackprinter = None
    IS_STACKPRINTER = False
from entest.const import STATUS, display

if IS_RICH:
    console = Console()
    stderr_console = Console(stderr=True)

    def logger(*args) -> None:
        console.print(*args)

    def stderr_logger(*args) -> None:
        stderr_console.print(*args)

else:

    def logger(*args) -> None:
        print(" ".join(args))

    def stderr_logger(*args) -> None:
        print(*args, file=stderr)


def generate_table(order: list) -> Table:
    """Make a new table."""
    table = Table()
    table.add_column("Status")
    table.add_column("Test Name")
    for test in order:
        table.add_row(display(test.status), f"{' ' * test.depth}{test.name()}")
    return table


def poor_panel(order, logger):
    pending_tests = order.copy()
    while any(test.status in (STATUS.wait, STATUS.running) for test in order):
        just_finished_tests = filter(
            lambda test: test.status not in (STATUS.wait, STATUS.running),
            pending_tests,
        )
        for test in just_finished_tests:
            logger(test.display())
            pending_tests.remove(test)
        time.sleep(0.4)


def rich_panel(order):
    with Live(generate_table(order), refresh_per_second=4) as live:
        while any(test.status in (STATUS.wait, STATUS.running) for test in order):
            time.sleep(0.4)
            live.update(generate_table(order))


class StatusPanel:
    def __init__(self, order, logger):
        if IS_RICH:
            self.thread = threading.Thread(target=rich_panel, args=(order,))
        else:
            self.thread = threading.Thread(target=poor_panel, args=(order, logger))

    def __enter__(self):
        self.thread.start()

    def __exit__(self, *args):
        self.thread.join(timeout=1)


def format_error(error: Exception):
    if IS_STACKPRINTER:
        return stackprinter.format(error, style="darkbg3")
    if IS_RICH:
        return Traceback(Traceback.extract(type(error), error, error.__traceback__))
    else:
        return type(error).__name__ + "\n" + "".join(format_tb(error.__traceback__))
