"""Handle re-computation of values of a function given its abstract syntax tree and function frame."""

import ast
import builtins
import copy
import functools
import inspect
import sys
import uuid
from typing import (
    Any,
    Mapping,
    Dict,
    List,
    Optional,
    Union,
    Tuple,
    Set,
    Callable,
    cast,
    Iterable,
    TypeVar,
)  # pylint: disable=unused-import

from _ast import If


class Placeholder:
    """Represent a placeholder for variables local to the lambda such as targets in generator expressions."""

    def __repr__(self) -> str:
        """Represent the placeholder as <Placeholder>."""
        return "<Placeholder>"


PLACEHOLDER = Placeholder()


class FirstExceptionInAll:
    """Represent a first exception case for which an all quantifier does not apply."""

    def __init__(self, result: Any, inputs: Tuple[Tuple[str, Any]]) -> None:
        """
        Initialize with the given values.

        :param result: value of the evaluation which was not truthy
        :param inputs: all the target loop variables set during the iteration
        """
        self.result = result
        self.inputs = inputs

    def __bool__(self) -> Any:
        """Return the result of the ELT evaluation which invalidated the ``all`` quantifier."""
        return self.result


ContextT = TypeVar("ContextT", bound=ast.expr_context)


class _CollectStoredNamesVisitor(ast.NodeVisitor):
    """Traverse the abstract syntax tree and collect all the names which are stored."""

    def __init__(self) -> None:
        self.names = []  # type: List[str]
        self._name_set = set()  # type: Set[str]

    def visit_Name(self, node: ast.Name) -> Any:  # pylint: disable=invalid-name
        """Collect the name if it is in a store context."""
        pass


def _collect_stored_names(nodes: Iterable[ast.expr]) -> List[str]:
    pass


class _CollectNameLoadsVisitor(ast.NodeVisitor):
    """Traverse the abstract syntax tree and collect all the name nodes in Load context."""

    def __init__(self) -> None:
        self.nodes = []  # type: List[ast.expr]

    def visit_Name(self, node: ast.Name) -> Any:  # pylint: disable=invalid-name
        """Collect the name if it is in a load context."""
        pass


def _collect_name_loads(nodes: Iterable[ast.expr]) -> List[ast.expr]:
    pass


# noinspection PyTypeChecker
def _translate_all_expression_to_a_module(
    generator_exp: ast.GeneratorExp,
    generated_function_name: str,
    name_to_value: Mapping[str, Any],
) -> ast.Module:
    """
    Generate the AST of the module to trace an all quantifier on an generator expression.

    :param generator_exp: generator expression to be translated
    :param generated_function_name: UUID of the tracing function to be used in the code
    :param name_to_value:
        mapping of all resolved values to the variable names
        (passed as arguments to the function so that the generation can access them)
    :return: translation to a module
    """
    pass


# noinspection PyTypeChecker
class Visitor(ast.NodeVisitor):
    """
    Traverse the abstract syntax tree and recompute the values of each node defined by the function frame.

    :ivar recomputed_values: mapping node -> value assigned to each visited node
    :type recomputed_values: Mapping[ast.AST, Any]
    """

    # pylint: disable=invalid-name
    # pylint: disable=missing-docstring

    def __init__(self, variable_lookup: List[Mapping[str, Any]]) -> None:
        """
        Initialize.

        :param variable_lookup: list of lookup tables to look-up the values of the variables, sorted by precedence
        """
        # _name_to_value maps the variable names to variable values.
        # This is important for Load contexts as well as Store contexts in, e.g., named expressions.
        self._name_to_value = dict()  # type: Dict[str, Any]

        # Resolve precedence of variable lookups
        for lookup in variable_lookup:
            for name, value in lookup.items():
                if name not in self._name_to_value:
                    self._name_to_value[name] = value

        # value assigned to each visited node
        self.recomputed_values = dict()  # type: Dict[ast.AST, Any]

    if sys.version_info < (3, 8):

        def visit_Num(self, node: ast.Num) -> Union[int, float]:
            """Recompute the value as the number at the node."""
            pass

        def visit_Str(self, node: ast.Str) -> str:
            """Recompute the value as the string at the node."""
            pass

        def visit_Bytes(self, node: ast.Bytes) -> bytes:
            """Recompute the value as the bytes at the node."""
            pass

        def visit_NameConstant(self, node: ast.NameConstant) -> Any:
            """Forward the node value as a result."""
            pass

    else:

        def visit_Constant(self, node: ast.Constant) -> Any:
            """Forward the node value as a result."""
            pass

    if sys.version_info >= (3, 6):

        def visit_FormattedValue(
            self, node: ast.FormattedValue
        ) -> Union[str, Placeholder]:
            """Format the node value."""
            pass

        def visit_JoinedStr(self, node: ast.JoinedStr) -> Union[str, Placeholder]:
            """Visit the values and concatenate them."""
            pass

    def visit_List(self, node: ast.List) -> Union[List[Any], Placeholder]:
        """Visit the elements and assemble the results into a list."""
        pass

    def visit_Tuple(self, node: ast.Tuple) -> Union[Tuple[Any, ...], Placeholder]:
        """Visit the elements and assemble the results into a tuple."""
        pass

    def visit_Set(self, node: ast.Set) -> Union[Set[Any], Placeholder]:
        """Visit the elements and assemble the results into a set."""
        pass

    def visit_Dict(self, node: ast.Dict) -> Union[Dict[Any, Any], Placeholder]:
        """Visit keys and values and assemble a dictionary with the results."""
        pass

    def visit_Name(self, node: ast.Name) -> Any:
        """Load the variable by looking it up in the variable look-up and in the built-ins."""
        pass

    def visit_Expr(self, node: ast.Expr) -> Any:
        """Visit the node's ``value``."""
        pass

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Any:
        """Visit the node operand and apply the operation on the result."""
        pass

    def visit_BinOp(self, node: ast.BinOp) -> Any:
        """Recursively visit the left and right operand, respectively, and apply the operation on the results."""
        pass

    def visit_BoolOp(self, node: ast.BoolOp) -> Any:
        """Recursively visit the operands and apply the operation on them."""
        pass

    def visit_Compare(self, node: ast.Compare) -> Any:
        """Recursively visit the comparators and apply the operations on them."""
        pass

    def visit_Call(self, node: ast.Call) -> Any:
        """Visit the function and the arguments and finally make the function call with them."""
        pass

    def visit_IfExp(self, node: ast.IfExp) -> Any:
        """Visit the ``test``, and depending on its outcome, the ``body`` or ``orelse``."""
        pass

    def visit_Attribute(self, node: ast.Attribute) -> Any:
        """Visit the node's ``value`` and get the attribute from the result."""
        pass

    if sys.version_info >= (3, 8):

        def visit_NamedExpr(self, node: ast.NamedExpr) -> Any:
            """Visit the node's ``value`` and assign it to both this node and the target."""
            pass

    if sys.version_info < (3, 9):

        def visit_Index(self, node: ast.Index) -> Any:
            """Visit the node's ``value``."""
            pass

    def visit_Slice(self, node: ast.Slice) -> Union[slice, Placeholder]:
        """Visit ``lower``, ``upper`` and ``step`` and recompute the node as a ``slice``."""
        pass

    if sys.version_info < (3, 9):

        def visit_ExtSlice(
            self, node: ast.ExtSlice
        ) -> Union[Tuple[Any, ...], Placeholder]:
            """Visit each dimension of the advanced slicing and assemble the dimensions in a tuple."""
            pass

    def visit_Subscript(self, node: ast.Subscript) -> Any:
        """Visit the ``slice`` and a ``value`` and get the element."""
        pass

    def _trace_all_with_generator(
        self, func: Callable[..., Any], node: ast.Call
    ) -> Any:
        """Re-write the all call with for loops to trace the first offending item, if any."""
        pass

    def _execute_comprehension(
        self, node: Union[ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp]
    ) -> Any:
        """Compile the generator or comprehension from the node and execute the compiled code."""
        pass

    def visit_GeneratorExp(self, node: ast.GeneratorExp) -> Any:
        """Compile the generator expression as a function and call it."""
        pass

    def visit_ListComp(self, node: ast.ListComp) -> Any:
        """Compile the list comprehension as a function and call it."""
        pass

    def visit_SetComp(self, node: ast.SetComp) -> Any:
        """Compile the set comprehension as a function and call it."""
        pass

    def visit_DictComp(self, node: ast.DictComp) -> Any:
        """Compile the dictionary comprehension as a function and call it."""
        pass

    def visit_Lambda(self, node: ast.Lambda) -> Callable[..., Any]:
        """Do not support inline lambda until there is a feature request since this is quite tricky to implement."""
        raise NotImplementedError(
            "Re-computation of in-line lambda functions is not supported since it is quite tricky to implement and "
            "we decided to implement it only once there is a real need for it. "
            "Please make a feature request on https://github.com/Parquery/icontract"
        )

    def visit_Return(self, node: ast.Return) -> Any:
        """Raise an exception that this node is unexpected."""
        raise AssertionError(
            "Unexpected return node during the re-computation: {}".format(
                ast.dump(node)
            )
        )

    def generic_visit(self, node: ast.AST) -> None:
        """Raise an exception that this node has not been handled."""
        raise NotImplementedError(
            "Unhandled re-computation of the node: {} {}".format(type(node), node)
        )
