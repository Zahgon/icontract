"""Handle representations necessary for informative error messages."""

import ast
import inspect
import re
import reprlib
import sys
import textwrap
import uuid
from typing import (
    Any,
    Mapping,
    MutableMapping,
    Callable,
    List,
    Dict,
    cast,
    Optional,
)  # pylint: disable=unused-import

import asttokens.asttokens

import icontract._recompute
from icontract._types import Contract
from icontract._globals import CallableT

# pylint does not play with typing.Mapping.
# pylint: disable=unsubscriptable-object


def _representable(value: Any) -> bool:
    """
    Check whether we want to represent the value in the error message on contract breach.

    We do not want to represent classes, methods, modules and functions.

    :param value: value related to an AST node
    :return: True if we want to represent it in the violation error
    """
    pass


class Visitor(ast.NodeVisitor):
    """Traverse the abstract syntax tree and collect the representations of the selected nodes."""

    # pylint: disable=invalid-name
    # pylint: disable=missing-docstring

    def __init__(
        self,
        recomputed_values: Mapping[ast.AST, Any],
        variable_lookup: List[Mapping[str, Any]],
        atok: asttokens.asttokens.ASTTokens,
    ) -> None:
        """
        Initialize.

        :param recomputed_values: AST node of a condition function -> value associated with the node
        :param variable_lookup:
            list of lookup tables to look-up the values of the variables, sorted by precedence.
            The visitor needs it here to check whether we overrode a built-in variable (like ``id``).
        :param atok: parsed AST tree and tokens with additional positions in source code

        """
        self._recomputed_values = recomputed_values
        self._variable_lookup = variable_lookup
        self.reprs = dict()  # type: MutableMapping[str, str]
        self._atok = atok

    if sys.version_info >= (3, 6):

        def visit_JoinedStr(self, node: ast.JoinedStr) -> None:
            """Show the whole joined strings without descending into the values."""
            pass

    def visit_Name(self, node: ast.Name) -> None:
        """
        Resolve the name from the variable look-up and the built-ins.

        Due to possible branching (e.g., If-expressions), some nodes might lack the recomputed values. These nodes
        are ignored.
        """
        pass

    def visit_Attribute(self, node: ast.Attribute) -> None:
        """Represent the attribute by dumping its source code."""
        pass

    if sys.version_info >= (3, 8):

        def visit_NamedExpr(self, node: ast.NamedExpr) -> Any:
            """Represent the target with the value of the node."""
            pass

    def visit_Call(self, node: ast.Call) -> None:
        """Represent the call by dumping its source code."""
        pass

    def visit_ListComp(self, node: ast.ListComp) -> None:
        """Represent the list comprehension by dumping its source code."""
        pass

    def visit_SetComp(self, node: ast.SetComp) -> None:
        """Represent the set comprehension by dumping its source code."""
        pass

    def visit_DictComp(self, node: ast.DictComp) -> None:
        """Represent the dictionary comprehension by dumping its source code."""
        pass

    def visit_Subscript(self, node: ast.Subscript) -> None:
        """Represent the subscript with its source code."""
        pass


def is_lambda(a_function: CallableT) -> bool:
    """
    Check whether the function is a lambda function.

    >>> def some_func()->bool: return True
    >>> is_lambda(some_func)
    False

    >>> lmbd = lambda x: x > 0
    >>> is_lambda(lmbd)
    True

    :return: True if condition is defined as lambda function
    """
    pass


class ConditionLambdaInspection:
    """Represent the inspection of the condition function given as a lambda."""

    def __init__(self, atok: asttokens.asttokens.ASTTokens, node: ast.Lambda) -> None:
        """
        Initialize.

        :param atok: parsed AST tree and tokens with added positional properties
        :param node: lambda AST node corresponding to the condition
        """
        self.atok = atok
        self.node = node

        text = atok.get_text(node.body)
        assert isinstance(text, str)
        self.text = text


_DECORATOR_RE = re.compile(r"^\s*@[a-zA-Z_]")
_DEF_CLASS_RE = re.compile(r"^\s*(async\s+def|def |class )")


class DecoratorInspection:
    """Represent the inspection of a decorator extracted from a source file and embedded in a dummy dynamic module."""

    def __init__(self, atok: asttokens.asttokens.ASTTokens, node: ast.Call) -> None:
        """
        Initialize.

        :param atok: parsed AST tree and tokens with added positional properties
        :param node: lambda AST node corresponding to the condition
        """
        self.atok = atok
        self.node = node


def inspect_decorator(
    lines: List[str], lineno: int, filename: str
) -> DecoratorInspection:
    """
    Parse the file in which the decorator is called and figure out the corresponding call AST node.

    :param lines: lines of the source file corresponding to the decorator call
    :param lineno: line index (starting with 0) of one of the lines in the decorator call
    :param filename: name of the file where decorator is called
    :return: inspected decorator call
    """
    pass


def find_lambda_condition(
    decorator_inspection: DecoratorInspection,
) -> Optional[ConditionLambdaInspection]:
    """
    Inspect the decorator and extract the condition as lambda.

    If the condition is not given as a lambda function, return None.
    """
    pass


def inspect_lambda_condition(
    condition: Callable[..., Any],
) -> Optional[ConditionLambdaInspection]:
    """
    Try to extract the source code of the condition as lambda.

    If the condition is not a lambda, returns None.
    """
    pass


# fmt: off
def collect_variable_lookup(
        condition: Callable[..., Any],
        resolved_kwargs: Optional[Mapping[str, Any]] = None
) -> List[Mapping[str, Any]]:
    """
    Collect the variable lookups in order of precedence.

    :param condition: contract condition for which we are constructing a variable look-up tables
    :param resolved_kwargs:
        keyword arguments of the original function to be passed over to the condition (where applicable).

        The keyword arguments are added to the variable look-up tables accordingly.
        If ``resolved_kwargs`` is None, no keyword arguments will be added to the variable look-up table.
    """
    pass


def repr_values(condition: Callable[..., bool], lambda_inspection: Optional[ConditionLambdaInspection],
                resolved_kwargs: Mapping[str, Any], a_repr: reprlib.Repr) -> List[str]:
    """
    Represent function arguments and frame values in the error message on contract breach.

    :param condition: condition function of the contract
    :param lambda_inspection:
        inspected lambda AST node corresponding to the condition function (None if the condition was not given as a
        lambda function)
    :param resolved_kwargs: arguments put in the function call
    :param a_repr: representation instance that defines how the values are represented.
    :return: list of value representations
    """
    pass


def represent_condition(condition: CallableT) -> str:
    """Represent the condition as a string."""
    pass


def generate_message(contract: Contract, resolved_kwargs: Mapping[str, Any]) -> str:
    """Generate the message upon contract violation."""
    pass
