"""Static code analysis for mutable object safety in Python"""

import typing as _typing

_T = _typing.TypeVar("_T")


class Mut(_typing.Generic[_T]):
    """Type handled by mypy plugin"""

    pass


__all__: _typing.List[str] = [
    "Mut",
]
