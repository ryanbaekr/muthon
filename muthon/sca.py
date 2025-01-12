"""Entry point for running SCA"""

from typing import Optional, TypedDict, Unpack

import libcst as cst
from libcst.metadata import ScopeProvider, PositionProvider


class KeyWordArgs(TypedDict):
    module: Optional[str]
    package: Optional[str]
    exclude: Optional[str]
    verbose: bool


class MuthonError(Exception):
    pass


class muthonVisitor(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (ScopeProvider, PositionProvider)

    def __init__(self) -> None:
        self._muthon_scopes: dict[str, dict[str, str]] = {}
        super().__init__()

    def visit_Assign(self, node: cst.Assign) -> None:
        scope = self.get_metadata(ScopeProvider, node)
        var_name: str = ""
        for child in node.children:
            if isinstance(child, cst.AssignTarget):
                for target in child.children:
                    if isinstance(target, cst.Name):
                        var_name = target.value
        if scope is not None and hasattr(scope, "name") and scope.name in self._muthon_scopes and var_name in self._muthon_scopes[scope.name]:
            return
        if var_name:
            raise MuthonError(f"Variable: {var_name} initialized without type")

    def visit_AnnAssign(self, node: cst.AnnAssign) -> None:
        var_name: str = ""
        var_type: str | None = None
        for child in node.children:
            if isinstance(child, cst.Name):
                var_name = child.value
            elif isinstance(child, cst.Annotation) and hasattr(child.annotation, "value"):
                if hasattr(child.annotation.value, "value"):
                    var_type = child.annotation.value.value
                else:
                    var_type = child.annotation.value
        if var_name and var_type is None:
            raise MuthonError(f"Variable: {var_name} initialized without type")

    def visit_Call(self, node: cst.Call) -> None:
        # Get the scope of the call
        scope = self.get_metadata(ScopeProvider, node)
        for arg in node.args:
            if isinstance(arg.value, cst.Name):
                var_name: str = arg.value.value
                if scope is None:
                    continue
                assigns = scope[var_name]
                # TODO check type of assignment
                for assign in assigns:
                    if not (isinstance(assign, cst.metadata.Assignment) and isinstance(assign.node, cst.Name)):
                        continue
                    # get position data from assign
                    pos = self.get_metadata(PositionProvider, assign.node)
                    print(f"{assign.node.value} found at line {pos.start.line}, column {pos.start.column}")

    def visit_FunctionDef(self, node: cst.FunctionDef) -> None:
        for child in node.children:
            if isinstance(child, cst.Parameters):
                for param in child.children:
                    if not hasattr(param, "name"):
                        continue
                    param_name: str = param.name.value
                    if hasattr(param, "annotation"):
                        param_type = param.annotation.annotation.value
                        try:
                            self._muthon_scopes[node.name.value][param_name] = param_type
                        except KeyError:
                            self._muthon_scopes[node.name.value] = {param_name: param_type}
                    else:
                        raise MuthonError(f"Parameter: {param_name} is not typed")


def parse_file(file: str, verbose: bool) -> bool:
    """Parse syntax tree of individual file"""
    with open(file) as f:
        try:
            source_tree = cst.parse_module(f.read())
            wrapper = cst.MetadataWrapper(source_tree)
            result = wrapper.visit(muthonVisitor())
            #print(result)
        except cst.ParserSyntaxError as syntax:
            #print(syntax)
            return False
        except MuthonError:
            return False

    return True


def run_sca(**kwargs: Unpack[KeyWordArgs]) -> bool:
    """Execute SCA on the provided code"""

    sources, verbose = process_args(**kwargs)

    for file in sources:
        if not parse_file(file, verbose):
            return False

    return True


def process_args(module: Optional[str]=None, package: Optional[str]=None, exclude: Optional[str]=None, verbose: bool=False) -> tuple[list[str], bool]:
    """Process args and handle errors"""

    if module is None and package is None:
        raise

    if module is not None:
        return [module], verbose

    return [], verbose
