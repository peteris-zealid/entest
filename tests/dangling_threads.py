import subprocess
import threading
from time import sleep

from entest import depends_on
from entest.runner import join_dangling_threads

# This file consists of 2 parts that are expected to run in 2 separate proceses.
# You can think of these as 2 separate files that are tightly related.
# Part 1 is run by entest process
# Part 2 is spawned in a new python process from entest process.

# Part 1:
@depends_on()
def close_threads_automatically():
    result = run_this_file()
    assert result.returncode == -6
    assert result.stdout == (
        b"Found 2 dangling threads.\n" b"Some non-daemon threads could not be joined.\n"
    )


def run_this_file():
    return subprocess.run(["python3", "tests/dangling_threads.py"], capture_output=True)


# Part 2:
def main():
    threading.Thread(target=sleep, args=[0]).start()  # normal_thread
    threading.Thread(target=sleep, args=[1234], daemon=True).start()  # daemon_thread
    threading.Thread(target=sleep, args=[1234]).start()  # unjoined_thread
    join_dangling_threads(print)


if __name__ == "__main__":
    main()
