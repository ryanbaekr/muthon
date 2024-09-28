"""Entry point for running SCA"""

from typing import Optional, TypedDict, Unpack

import libcst as cst
from libcst.metadata import ScopeProvider, PositionProvider

class KeyWordArgs(TypedDict):
    module: Optional[str]
    package: Optional[str]
    exclude: Optional[str]
    verbose: bool


class muthonVisitor(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (ScopeProvider, PositionProvider)

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

def parse_file(file: str) -> Optional[cst.Module]:
    """Parse syntax tree of individual file"""
    with open(file) as f:
        try:
            source_tree = cst.parse_module(f.read())
            wrapper = cst.MetadataWrapper(source_tree)
            result = wrapper.visit(muthonVisitor())
            #print(result)
        except cst.ParserSyntaxError as syntax:
            print(syntax)
            source_tree = None
    return source_tree


def run_sca(**kwargs: Unpack[KeyWordArgs]) -> bool:

    """Execute SCA on the provided code"""

    sources, verbose = process_args(**kwargs)

    print(sources)
    for file in sources:
        print(parse_file(file))

    print(verbose)

    return True


def process_args(module: Optional[str]=None, package: Optional[str]=None, exclude: Optional[str]=None, verbose: bool=False) -> tuple[list[str], bool]:
    """Process args and handle errors"""

    if module is None and package is None:
        raise

    if module is not None:
        return [module], verbose

    return [], verbose
