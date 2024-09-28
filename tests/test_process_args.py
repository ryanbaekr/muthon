"""Testing Argument Processing"""

from muthon.sca import process_args
from muthon.sca import KeyWordArgs

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
