#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path

from entest.const import STATUS
from entest.dependency_decorator import TestCase, test_discovery
from entest.graph import graph
from entest.runner import run_tests
from entest.snoop import setup_snooper
from entest.status_report import logger, stderr_logger

parser = argparse.ArgumentParser(description='Run integration tests.')
parser.add_argument('paths', type=str, nargs="*", help='files to run')
parser.add_argument('--graph', action="store_true", help="Print Mermaid diagram of the test tree")
parser.add_argument(
    '--snoop',
    default="",
    const="std",
    nargs="?",
    help="Print automatic debugging to a file or terminal if no file is provided",
)
parser.add_argument(
    '--env', default="", help="Sets TEST_ENV_NAME env variable used by env/loader.py"
)
parser.add_argument(
    '--skip-teardown', action="store_true", help="Do not run test cases that have `run_last=True`"
)


def main():
    args = parser.parse_args()
    if args.env:
        os.environ["TEST_ENV_NAME"] = args.env
    if args.skip_teardown:
        os.environ["ENTEST_SKIP_TEARDOWN"] = "yes"
    if args.snoop:
        setup_snooper(args.snoop)
    paths = [Path(path) for path in args.paths]
    test_discovery(paths, stderr_logger)
    if args.graph:
        logger(graph())
        sys.exit(0)
    run_tests(logger)
    sys.exit(TestCase.summary(as_dict=True)[STATUS.error])


if __name__ == '__main__':
    main()
