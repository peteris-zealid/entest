__all__ = ["depends_on", "setup_setup", "STATUS", "assert_raises"]
from typing import Callable

from .const import STATUS
from .dependency_decorator import depends_on, setup_setup


def assert_raises(cb: Callable, message="") -> Exception:
    try:
        cb()
    except Exception as err:
        assert message in str(err)
        return err
    raise Exception("Function did not raise Exception")
