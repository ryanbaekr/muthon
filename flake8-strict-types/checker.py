"""Force a type annotation on every assignment"""

import ast
from typing import Any, Generator, List, Tuple, Type


class StrictTypeVisitor(ast.NodeVisitor):
    def __init__(self, errors: List[Tuple[int, int, str]]) -> None:
        self.errors: List[Tuple[int, int, str]] = errors

    def visit_Assign(self, node: ast.Assign) -> None:
        """Flag standard assignments like 'x = 1'"""
        self.errors.append((
            node.lineno,
            node.col_offset,
            "TYP001 missing type annotation for variable",
        ))
        self.generic_visit(node)


class Plugin:
    name: str = "flake8-strict-types"
    version: str = "0.1.0"

    def __init__(self, tree: ast.AST) -> None:
        self.tree: ast.AST = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        errors: List[Tuple[int, int, str]] = []
        visitor: StrictTypeVisitor = StrictTypeVisitor(errors=errors)
        visitor.visit(self.tree)
        for lineno, colno, msg in errors:
            yield lineno, colno, msg, type(self)
