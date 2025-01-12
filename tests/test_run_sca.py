"""Testing Static Code Analysis"""

import os

from muthon.sca import run_sca
from muthon.sca import KeyWordArgs

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
