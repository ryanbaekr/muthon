"""Allow mypy to unpack the type inside Mut[]"""

from typing import Any, Callable, Optional
from mypy.plugin import Plugin, AnalyzeTypeContext
from mypy.types import Type as MypyType


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

    return inner_type if inner_type is not None else ctx.type.args[0]


def plugin(version: str) -> Any:
    return MutPlugin
