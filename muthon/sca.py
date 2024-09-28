"""Entry point for running SCA"""

def run_sca(**kwargs):
    """Execute SCA on the provided code"""

    sources, verbose = process_args(**kwargs)

    print(sources)
    print(verbose)

    return True


def process_args(module=None, package=None, exclude=None, verbose=False):
    """Process args and handle errors"""

    if module is None and package is None:
        raise

    return [], verbose
