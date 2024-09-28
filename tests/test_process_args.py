"""Testing Argument Processing"""

import os

from muthon.sca import process_args
from muthon.sca import KeyWordArgs
from muthon.sca import run_sca

def test_module_only() -> None:
    """Test process_args with only a module arg"""

    kwargs: KeyWordArgs = {
        "module": "module.py",
        "package": None,
        "exclude": None,
        "verbose": False,
    }

    sources, verbose = process_args(**kwargs)

    assert len(sources) == 1
    assert sources[0] == "module.py"

    assert verbose is False


def test_sca_only() -> None:
    """Test run_sca with only a module arg"""

    kwargs: KeyWordArgs = {
        "module": os.path.realpath("tests/fixtures/mutable_in.py"),
        "package": None,
        "exclude": None,
        "verbose": False,
    }

    result = run_sca(**kwargs)

    assert result