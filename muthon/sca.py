"""Entry point for running SCA"""

from typing import Optional, TypedDict, Unpack

class KeyWordArgs(TypedDict):
    module: Optional[str]
    package: Optional[str]
    exclude: Optional[str]
    verbose: bool

def run_sca(**kwargs: Unpack[KeyWordArgs]) -> bool:

    """Execute SCA on the provided code"""

    sources, verbose = process_args(**kwargs)

    print(sources)
    print(verbose)

    return True


def process_args(module: Optional[str]=None, package: Optional[str]=None, exclude: Optional[str]=None, verbose: bool=False) -> tuple[list[str], bool]:
    """Process args and handle errors"""

    if module is None and package is None:
        raise

    if module is not None:
        return [module], verbose

    return [], verbose
