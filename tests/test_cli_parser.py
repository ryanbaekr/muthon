"""Testing the CLI Parser"""

from muthon.cli_parser import parse_args

def test_module_only() -> None:
    """Test cli_parser with only a module arg"""

    args = [
        "--module",
        "module.py",
    ]

    kwargs = parse_args(args)

    keys = list(kwargs.keys())
    assert len(keys) == 4
    assert keys[0] == "module"
    assert keys[1] == "package"
    assert keys[2] == "exclude"
    assert keys[3] == "verbose"

    assert kwargs["module"] == "module.py"
    assert kwargs["package"] is None
    assert kwargs["exclude"] is None
    assert kwargs["verbose"] is False

    args = [
        "-m",
        "module.py",
    ]

    kwargs = parse_args(args)

    keys = list(kwargs.keys())
    assert len(keys) == 4
    assert keys[0] == "module"
    assert keys[1] == "package"
    assert keys[2] == "exclude"
    assert keys[3] == "verbose"

    assert kwargs["module"] == "module.py"
    assert kwargs["package"] is None
    assert kwargs["exclude"] is None
    assert kwargs["verbose"] is False


def test_package_only() -> None:
    """Test cli_parser with only a package arg"""

    args = [
        "--package",
        "package/",
    ]

    kwargs = parse_args(args)

    keys = list(kwargs.keys())
    assert len(keys) == 4
    assert keys[0] == "module"
    assert keys[1] == "package"
    assert keys[2] == "exclude"
    assert keys[3] == "verbose"

    assert kwargs["module"] is None
    assert kwargs["package"] == "package/"
    assert kwargs["exclude"] is None
    assert kwargs["verbose"] is False

    args = [
        "-p",
        "package/",
    ]

    kwargs = parse_args(args)

    keys = list(kwargs.keys())
    assert len(keys) == 4
    assert keys[0] == "module"
    assert keys[1] == "package"
    assert keys[2] == "exclude"
    assert keys[3] == "verbose"

    assert kwargs["module"] is None
    assert kwargs["package"] == "package/"
    assert kwargs["exclude"] is None
    assert kwargs["verbose"] is False


def test_module_and_package() -> None:
    """Test the invalid combination of module and package"""

    args = [
        "--module",
        "module.py",
        "--package",
        "package/",
    ]

    try:
        parse_args(args)
        assert False
    except SystemExit:
        assert True


def test_no_args() -> None:
    """Test the invalid case of no args"""

    args: list[str] = []

    try:
        parse_args(args)
        assert False
    except SystemExit:
        assert True


def test_exclude() -> None:
    """Test the exclude arg"""

    args = [
        "--module",
        "module.py",
        "--exclude",
        "regex",
    ]

    kwargs = parse_args(args)

    keys = list(kwargs.keys())
    assert len(keys) == 4
    assert keys[0] == "module"
    assert keys[1] == "package"
    assert keys[2] == "exclude"
    assert keys[3] == "verbose"

    assert kwargs["module"] == "module.py"
    assert kwargs["package"] is None
    assert kwargs["exclude"] == "regex"
    assert kwargs["verbose"] is False

    args = [
        "--package",
        "package/",
        "-e",
        "regex",
    ]

    kwargs = parse_args(args)

    keys = list(kwargs.keys())
    assert len(keys) == 4
    assert keys[0] == "module"
    assert keys[1] == "package"
    assert keys[2] == "exclude"
    assert keys[3] == "verbose"

    assert kwargs["module"] is None
    assert kwargs["package"] == "package/"
    assert kwargs["exclude"] == "regex"
    assert kwargs["verbose"] is False


def test_verbose() -> None:
    """Test the verbose arg"""

    args = [
        "--module",
        "module.py",
        "--verbose",
    ]

    kwargs = parse_args(args)

    keys = list(kwargs.keys())
    assert len(keys) == 4
    assert keys[0] == "module"
    assert keys[1] == "package"
    assert keys[2] == "exclude"
    assert keys[3] == "verbose"

    assert kwargs["module"] == "module.py"
    assert kwargs["package"] is None
    assert kwargs["exclude"] is None
    assert kwargs["verbose"] is True

    args = [
        "--package",
        "package/",
        "-v",
    ]

    kwargs = parse_args(args)

    keys = list(kwargs.keys())
    assert len(keys) == 4
    assert keys[0] == "module"
    assert keys[1] == "package"
    assert keys[2] == "exclude"
    assert keys[3] == "verbose"

    assert kwargs["module"] is None
    assert kwargs["package"] == "package/"
    assert kwargs["exclude"] is None
    assert kwargs["verbose"] is True
