from typing import Callable, Optional, TypeVar

from entest.dependency_decorator import TestCase

F = TypeVar("F", bound=Callable)


def setup_snooper(output: Optional[str]) -> Callable[[F], F]:
    try:
        from pysnooper import snoop
    except ImportError as err:
        raise ImportError("You need to install optional dependency 'pysnooper' to snoop") from err

    if output == "std":
        TestCase.snoop_decorator = snoop()
    else:
        TestCase.snoop_decorator = snoop(output)
