"""Parser for the CLI"""

import argparse

from .constants import VERSION

def parse_args(args=None):
    """Return parsed args"""

    parser = argparse.ArgumentParser(
        prog="Muthon",
        description="Static code analysis for mutable object safety in Python",
        epilog=f"Muthon {VERSION}",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-m",
        "--module",
        action="store",
        default=None,
        dest="module",
        help="check module in the current directory",
        metavar="MODULE",
        required=False,
        type=str,
    )
    group.add_argument(
        "-p",
        "--package",
        action="store",
        default=None,
        dest="package",
        help="check package in the current directory",
        metavar="PACKAGE",
        required=False,
        type=str,
    )

    parser.add_argument(
        "-e",
        "--exclude",
        action="store",
        default=None,
        dest="exclude",
        help="regular expression to match files and directories that should be ignored",
        metavar="PATTERN",
        required=False,
        type=str,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        dest="verbose",
        help="more verbose messages",
        required=False,
    )

    args = parser.parse_args(args)

    return vars(args)
