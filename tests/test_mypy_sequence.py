"""Test the behavior of typing.Sequence"""

from typing import cast, MutableSequence, Sequence

from mutyping import Mut


def test_mut() -> None:
    """Test that Mut can be used in a type annotation"""

    x: Sequence[int] = [0, 1, 2]
    y: Mut[Sequence[int]] = [0, 1, 2]
    assert x == y


def test_readonly_mutable_sequence() -> None:
    """Test that mutable objects can be read"""

    def my_func(my_list: Sequence[int]) -> int:
        my_tot: int = 0

        for num in my_list:
            my_tot += num

        return my_tot

    x: MutableSequence[int] = [0, 1, 2]
    assert my_func(x) == 3  # noqa: PLR2004
    assert x == [0, 1, 2]


def test_mutation_mutable_sequence() -> None:
    """Test that mutable objects can be mutated"""

    def my_func(my_list: MutableSequence[int]) -> int:
        my_list.append(3)

        return len(my_list)

    x: MutableSequence[int] = [0, 1, 2]
    assert my_func(x) == 4  # noqa: PLR2004
    assert x == [0, 1, 2, 3]


def test_readonly_immutable_sequence() -> None:
    """Test that immutable objects can be read"""

    def my_func(my_list: Sequence[int]) -> int:
        my_tot: int = 0

        for num in my_list:
            my_tot += num

        return my_tot

    x: Sequence[int] = [0, 1, 2]
    assert my_func(x) == 3  # noqa: PLR2004
    assert x == [0, 1, 2]


def test_mutation_immutable_sequence() -> None:
    """Test that immutable objects can't be mutated"""

    def my_func(my_list: MutableSequence[int]) -> int:
        my_list.append(3)

        return len(my_list)

    x: Sequence[int] = [0, 1, 2]
    # the following executes at runtime, but is a mypy error
    assert my_func(x) == 4  # noqa: PLR2004
    assert x == [0, 1, 2, 3]


def test_mutation_immutable_sequence_w_cast() -> None:
    """Test that immutable objects can be mutated if first cast"""

    def my_func(my_list: MutableSequence[int]) -> int:
        my_list.append(3)

        return len(my_list)

    x: Sequence[int] = [0, 1, 2]
    assert my_func(cast(MutableSequence[int], x)) == 4  # noqa: PLR2004
    assert x == [0, 1, 2, 3]
