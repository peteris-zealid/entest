from collections import namedtuple
from typing import NamedTuple, NewType

StatusType = NewType("StatusType", str)


class Status(NamedTuple):
    wip: StatusType = StatusType("wip")
    none: StatusType = StatusType("none")
    wait: StatusType = StatusType("wait")
    running: StatusType = StatusType("running")
    deps_failed: StatusType = StatusType("deps_failed")
    passed: StatusType = StatusType("passed")
    error: StatusType = StatusType("error")


STATUS = Status()


def display(s: str) -> str:
    if s == STATUS.none:
        return "🤷 Ignored"
    elif s == STATUS.wait:
        return "⌛ Not run"
    elif s == STATUS.running:
        return "🏃 Running"
    elif s == STATUS.wip:
        return "🚧 WIP    "
    elif s == STATUS.deps_failed:
        return "⛔ Skipped"
    elif s == STATUS.passed:
        return "✅ Passed "
    elif s == STATUS.error:
        return "❌ Error  "
    else:
        return s
