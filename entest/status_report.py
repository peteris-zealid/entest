import random
import time

try:
    from rich.live import Live
    from rich.table import Table
    IS_RICH = True
except ImportError:
    IS_RICH = False

from entest.const import STATUS, display

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

def panel(order, logger):
    if IS_RICH:
        rich_panel(order)
    else:
        poor_panel(order, logger)
