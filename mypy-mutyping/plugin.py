"""Allow mypy to unpack the type inside Mut[]"""

from typing import Any, Callable, Dict, Optional
from mypy.plugin import Plugin, AnalyzeTypeContext
from mypy.types import Type as MypyType, Instance

MUTABLE_MAP: Dict[str, str] = {
    "typing.Sequence": "typing.MutableSequence",
    "typing.Mapping": "typing.MutableMapping",
    "typing.Set": "typing.MutableSet",
}


class MutPlugin(Plugin):
    def get_type_analyze_hook(
            self, fullname: str
    ) -> Optional[Callable[[AnalyzeTypeContext], MypyType]]:
        if fullname == "mutyping.Mut":
            return mut_type_analyze_callback

        return None


def mut_type_analyze_callback(ctx: AnalyzeTypeContext) -> MypyType:
    if not ctx.type.args:
        return ctx.api.named_type("builtins.any", [])

    inner_type: MypyType = ctx.api.analyze_type(ctx.type.args[0])

    if inner_type is None:
        return ctx.type.args[0]

    if isinstance(inner_type, Instance):
        base_fullname: str = inner_type.type.fullname

        if base_fullname in MUTABLE_MAP:
            return ctx.api.named_type(
                MUTABLE_MAP[base_fullname],
                [type for type in inner_type.args],
            )

    return inner_type


def plugin(version: str) -> Any:
    return MutPlugin
