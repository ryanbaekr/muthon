"""Testing Static Code Analysis"""

import os

from muthon.sca import parse_file

def test_no_type_annotation() -> None:
    """Test parse_file when a variable is initialized without a type"""

    result = parse_file(
        file=os.path.realpath("tests/fixtures/no_type.py"),
        verbose=False,
    )

    assert result is False


def test_mutable_in() -> None:
    """Test parse_file when a variable is mutable but is not modified"""

    result = parse_file(
        file=os.path.realpath("tests/fixtures/mutable_in.py"),
        verbose=False,
    )

    assert result


def test_mutable_inout() -> None:
    """Test parse_file when a variable is mutable and is modified"""

    result = parse_file(
        file=os.path.realpath("tests/fixtures/mutable_inout.py"),
        verbose=False,
    )

    assert result


def test_primitive_inout() -> None:
    """Test parse_file when a variable is primitive and is modified"""

    result = parse_file(
        file=os.path.realpath("tests/fixtures/primitive_inout.py"),
        verbose=False,
    )

    assert result
