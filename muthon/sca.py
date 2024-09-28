"""Entry point for running SCA"""

from typing import Optional, TypedDict, Unpack

import libcst as cst


class KeyWordArgs(TypedDict):
    module: Optional[str]
    package: Optional[str]
    exclude: Optional[str]
    verbose: bool


def parse_file(file: str) -> Optional[cst.Module]:
    """Parse syntax tree of individual file"""
    with open(file) as f:
        try:
            source_tree = cst.parse_module(f.read())
        except cst.ParserSyntaxError as syntax:
            print(syntax)
            source_tree = None
    return source_tree


def run_sca(**kwargs: Unpack[KeyWordArgs]) -> bool:

    """Execute SCA on the provided code"""

    sources, verbose = process_args(**kwargs)

    print(sources)
    for file in sources:
        print(parse_file(file))


    print(verbose)

    return True


def process_args(module: Optional[str]=None, package: Optional[str]=None, exclude: Optional[str]=None, verbose: bool=False) -> tuple[list[str], bool]:
    """Process args and handle errors"""

    if module is None and package is None:
        raise

    if module is not None:
        return [module], verbose

    return [], verbose
