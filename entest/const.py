from collections import namedtuple


def string_enum(*values: str, name="string_enum"):
    return namedtuple(name, values)(*values)


STATUS = string_enum("wip", "none", "wait", "running", "deps_failed", "passed", "error")


def display(s: str):
    if s == "none":
        return "🤷 Ignored"
    elif s == "wait":
        return "⌛ Not run"
    elif s == "running":
        return "🏃 Running"
    elif s == "wip":
        return "🚧 WIP    "
    elif s == "deps_failed":
        return "⛔ Skipped"
    elif s == "passed":
        return "✅ Passed "
    elif s == "error":
        return "❌ Error  "
    else:
        return s
