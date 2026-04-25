"""Define the metaclass necessary to inherit the contracts from the base classes."""

import abc
import inspect
import sys
import weakref
from typing import (
    List,
    MutableMapping,
    Any,
    Callable,
    Optional,
    cast,
    Set,
    Type,
    TypeVar,
)  # pylint: disable=unused-import

from icontract._types import Contract, Snapshot
import icontract._checkers

# Pylint can't deal with multiple Python versions and breaks on ``if``'s on method definitions.
# pylint: skip-file


def _collapse_invariants(
    bases: List[type], namespace: MutableMapping[str, Any], invariants_dunder: str
) -> None:
    """
    Collect invariants from the bases and merge them with the invariants in the namespace.

    We do not only collapse ``__invariants__`` class property, but we also need to collapse
    the filtered ``__invariants_on_call__`` and ``__invariants_on_setattr__``, as they are
    sub-lists of the ``__invariants__``.
    """
    pass

    # endregion


def _collapse_preconditions(
    base_preconditions: List[List[Contract]],
    bases_have_func: bool,
    preconditions: List[List[Contract]],
    func: Callable[..., Any],
) -> List[List[Contract]]:
    """
    Collapse function preconditions with the preconditions collected from the base classes.

    :param base_preconditions: preconditions collected from the base classes (grouped by base class)
    :param bases_have_func: True if one of the base classes has the function
    :param preconditions: preconditions of the function (before the collapse)
    :param func: function whose preconditions we are collapsing
    :return: collapsed sequence of precondition groups
    """
    pass


def _collapse_snapshots(
    base_snapshots: List[Snapshot], snapshots: List[Snapshot]
) -> List[Snapshot]:
    """
    Collapse snapshots of pre-invocation values with the snapshots collected from the base classes.

    :param base_snapshots: snapshots collected from the base classes
    :param snapshots: snapshots of the function (before the collapse)
    :return: collapsed sequence of snapshots
    """
    pass


def _collapse_postconditions(
    base_postconditions: List[Contract], postconditions: List[Contract]
) -> List[Contract]:
    """
    Collapse function postconditions with the postconditions collected from the base classes.

    :param base_postconditions: postconditions collected from the base classes
    :param postconditions: postconditions of the function (before the collapse)
    :return: collapsed sequence of postconditions
    """
    pass


def _decorate_namespace_function(
    bases: List[type], namespace: MutableMapping[str, Any], key: str
) -> None:
    """Collect preconditions and postconditions from the bases and decorate the function at the ``key``."""
    pass


def _decorate_namespace_property(
    bases: List[type], namespace: MutableMapping[str, Any], key: str
) -> None:
    """Collect contracts for all getters/setters/deleters corresponding to ``key`` and decorate them."""
    pass


def _dbc_decorate_namespace(
    bases: List[type], namespace: MutableMapping[str, Any]
) -> None:
    """
    Collect invariants, preconditions and postconditions from the bases and decorate all the methods.

    Instance methods are simply replaced with the decorated function/ Properties, class methods and static methods are
    overridden with new instances of ``property``, ``classmethod`` and ``staticmethod``, respectively.
    """
    pass


_CONTRACT_CLASSES = weakref.WeakSet()  # type: ignore

T = TypeVar("T")  # pylint: disable=invalid-name


def _register_for_hypothesis(cls: Type[T]) -> None:
    """
    Add ``cls`` to ``_CONTRACT_CLASSES`` to be later registered with icontract_hypothesis.

    icontract_hypothesis is expected to monkey-patch this function.
    Prior to patching, all the classes in ``_CONTRACT_CLASSES`` should be registered
    with Hypothesis.

    The registration is necessary so that the preconditions on the __init__ are propagated
    in ``hypothesis.strategies.builds``.
    """
    pass


class DBCMeta(abc.ABCMeta):
    """
    Define a meta class that allows inheritance of the contracts.

    The preconditions are weakened ("require else"), while postconditions ("ensure then") and invariants are
    strengthened according to the inheritance rules of the design-by-contract.
    """

    # We need to disable mcs check since ABCMeta doesn't follow the convention and calls the first argument ``mlcs``
    # instead of ``mcs``.
    # pylint: disable=bad-mcs-classmethod-argument

    if sys.version_info < (3,):
        raise NotImplementedError(
            "Python versions below not supported, got: {}".format(sys.version_info)
        )

    if sys.version_info < (3, 6):
        # pylint: disable=arguments-differ
        def __new__(mlcs, name, bases, namespace):
            """Create a class with inherited preconditions, postconditions and invariants."""
            _dbc_decorate_namespace(bases, namespace)

            cls = super().__new__(mlcs, name, bases, namespace)

            if hasattr(cls, "__invariants__"):
                icontract._checkers.add_invariant_checks(cls=cls)

            # This is necessary to avoid circular imports.
            # icontract-hypothesis depends on icontract and vice-versa.
            # This usually works since icontract-hypothesis does not use DBCMeta,
            # but blows up since icontract creates DBC with DBCMeta meta-class at the import time.
            if cls.__module__ != __name__:
                _register_for_hypothesis(cls)

            return cls

    else:

        def __new__(mlcs, name, bases, namespace, **kwargs):  # type: ignore
            """Create a class with inherited preconditions, postconditions and invariants."""
            _dbc_decorate_namespace(bases, namespace)

            cls = super().__new__(mlcs, name, bases, namespace, **kwargs)

            if hasattr(cls, "__invariants__"):
                icontract._checkers.add_invariant_checks(cls=cls)

            # This is necessary to avoid circular imports.
            # icontract-hypothesis depends on icontract and vice-versa.
            # This usually works since icontract-hypothesis does not use DBCMeta,
            # but blows up since icontract creates DBC with DBCMeta meta-class at the import time.
            if cls.__module__ != __name__:
                _register_for_hypothesis(cls)  # type: ignore

            return cls


class DBC(abc.ABC, metaclass=DBCMeta):
    """Provide a standard way to create a class which can inherit the contracts."""
