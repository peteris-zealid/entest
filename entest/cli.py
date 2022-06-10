#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path

from entest.dependency_decorator import test_discovery
from entest.graph import graph
from entest.runner import run_tests


def echo(*args):
    return print(" ".join(args))


parser = argparse.ArgumentParser(description='Run integration tests.')
parser.add_argument('paths', type=str, nargs="*", help='files to run')
parser.add_argument('--graph', action="store_true", help="Print Mermaid diagram of the test tree")
parser.add_argument(
    '--env', default="", help="Sets TEST_ENV_NAME env variable used by env/loader.py"
)


def main():
    args = parser.parse_args()
    if args.env:
        os.environ["TEST_ENV_NAME"] = args.env
    paths = [Path(path) for path in args.paths]
    test_discovery(paths, echo)
    if args.graph:
        echo(graph())
        sys.exit(0)
    run_tests(echo)
    sys.exit(0)


if __name__ == '__main__':
    main()
