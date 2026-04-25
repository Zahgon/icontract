"""Provide functions to add/find contract checkers."""

import contextvars
import functools
import inspect
from typing import (
    Callable,
    Any,
    Iterable,
    Optional,
    Tuple,
    List,
    Mapping,
    MutableMapping,
    Dict,
    cast,
    Set,
)

import icontract._represent
from icontract._globals import CallableT, ClassT
from icontract._types import Contract, Snapshot, InvariantCheckEvent
from icontract.errors import ViolationError


# pylint does not play with typing.Mapping.
# pylint: disable=unsubscriptable-object
# pylint: disable=raising-bad-type


def _walk_decorator_stack(func: CallableT) -> Iterable["CallableT"]:
    """
    Iterate through the stack of decorated functions until the original function.

    Assume that all decorators used functools.update_wrapper.
    """
    pass


def find_checker(func: CallableT) -> Optional[CallableT]:
    """Iterate through the decorator stack till we find the contract checker."""
    pass


def kwargs_from_call(
    param_names: List[str],
    kwdefaults: Dict[str, Any],
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> MutableMapping[str, Any]:
    """
    Inspect the input values received at the wrapper for the actual function call.

    :param param_names: parameter (*i.e.* argument) names of the original (decorated) function
    :param kwdefaults: default argument values of the original function
    :param args: arguments supplied to the call
    :param kwargs: keyword arguments supplied to the call
    :return: resolved arguments as they would be passed to the function
    """
    pass


def not_check(check: Any, contract: Contract) -> bool:
    """
    Negate the check value of a condition and capture missing boolyness (*e.g.*, when check is a numpy array).

    :param check: value of the evaluated condition
    :param contract: corresponding to the check
    :return: negated check
    :raise: ValueError if the check could not be negated
    """
    pass


def select_condition_kwargs(
    contract: Contract, resolved_kwargs: Mapping[str, Any]
) -> Mapping[str, Any]:
    """
    Select the keyword arguments that are used by the contract.

    :param contract: contract to be verified
    :param resolved_kwargs:
        resolved keyword arguments of the call (including the default argument values of the decorated function)
    :return: a subset of resolved_kwargs
    """
    pass


def _assert_no_invalid_kwargs(kwargs: Any) -> Optional[TypeError]:
    """Check that kwargs of a function contain no unexpected arguments."""
    pass


def _unpack_pre_snap_posts(
    wrapper: CallableT,
) -> Tuple[List[List[Contract]], List[Snapshot], List[Contract]]:
    """Retrieve the preconditions, snapshots and postconditions defined for the given wrapper checker."""
    pass


def _assert_resolved_kwargs_valid(
    postconditions: List[Contract], resolved_kwargs: Mapping[str, Any]
) -> Optional[TypeError]:
    """Check that the resolved kwargs of a decorated function are valid."""
    pass


def _create_violation_error(
    contract: Contract, resolved_kwargs: Mapping[str, Any]
) -> BaseException:
    """Create the violation error based on the violated contract."""
    pass


async def _assert_preconditions_async(
    preconditions: List[List[Contract]], resolved_kwargs: Mapping[str, Any]
) -> Optional[BaseException]:
    """Assert that the preconditions of an async function hold."""
    pass


def _assert_preconditions(
    preconditions: List[List[Contract]],
    resolved_kwargs: Mapping[str, Any],
    func: CallableT,
) -> Optional[BaseException]:
    """Assert that the preconditions of a sync function hold."""
    pass


async def _capture_old_async(
    snapshots: List[Snapshot], resolved_kwargs: Mapping[str, Any]
) -> "Old":
    """Capture all snapshots of an async function and return the captured values bundled in an ``Old``."""
    pass


def _capture_old(
    snapshots: List[Snapshot], resolved_kwargs: Mapping[str, Any], func: CallableT
) -> "Old":
    """Capture all snapshots of a sync function and return the captured values bundled in an ``Old``."""
    pass


async def _assert_postconditions_async(
    postconditions: List[Contract], resolved_kwargs: Mapping[str, Any]
) -> Optional[BaseException]:
    """Assert that the postconditions of an async function hold."""
    pass


def _assert_postconditions(
    postconditions: List[Contract], resolved_kwargs: Mapping[str, Any], func: CallableT
) -> Optional[BaseException]:
    """Assert that the postconditions of a sync function hold."""
    pass


def _assert_invariant(contract: Contract, instance: Any) -> None:
    """Assert that the contract holds as a class invariant given the instance of the class."""
    pass


def select_capture_kwargs(
    a_snapshot: Snapshot, resolved_kwargs: Mapping[str, Any]
) -> Mapping[str, Any]:
    """
    Select the keyword arguments that are used by the snapshot capture.

    :param a_snapshot: snapshot to be captured
    :param resolved_kwargs: resolved keyword arguments (including the default values)
    :return: a subset of resolved_kwargs
    """
    pass


def select_error_kwargs(
    contract: Contract, resolved_kwargs: Mapping[str, Any]
) -> Mapping[str, Any]:
    """
    Select the keyword arguments that are used by the error creator of the contract.

    :param contract: contract that was violated and for which we want to generate an error
    :param resolved_kwargs: resolved keyword arguments (including the default values)
    :return: a subset of resolved_kwargs
    """
    pass


class Old:
    """
    Represent argument values before the function invocation.

    Recipe taken from http://code.activestate.com/recipes/52308-the-simple-but-handy-collector-of-a-bunch-of-named/
    """

    def __init__(self, mapping: Mapping[str, Any]) -> None:
        """Update the ``__dict__`` with the given mapping."""
        self.__dict__.update(mapping)

    def __getattr__(self, item: str) -> Any:
        """Raise an error as this ``item`` should not be in the ``__dict__``."""
        raise AttributeError(
            "The snapshot with the name {!r} is not available in the OLD of a postcondition. "
            "Have you decorated the function with a corresponding snapshot decorator?".format(
                item
            )
        )

    def __repr__(self) -> str:
        """Represent the old values with a string literal as user is unaware of the class."""
        return "a bunch of OLD values"


def resolve_kwdefaults(sign: inspect.Signature) -> Dict[str, Any]:
    """Resolve default values for the function arguments based on its signature."""
    pass


# This flag is used to avoid recursively checking contracts for the same function or instance while
# contract checking is already in progress.
#
# The key refers to the id() of the function (preconditions and postconditions) or instance (invariants).
_IN_PROGRESS = contextvars.ContextVar(
    "_IN_PROGRESS", default=None
)  # type: contextvars.ContextVar[Optional[Set[int]]]


def decorate_with_checker(func: CallableT) -> CallableT:
    """Decorate the function with a checker that verifies the preconditions and postconditions."""
    pass


def add_precondition_to_checker(checker: CallableT, contract: Contract) -> None:
    """
    Add the precondition to the function's checker.

    Use :func:`find_checker` to find the checker.
    If it returns ``None``, decorate it with the checker first using :func:`decorate_with_checker`.
    """
    pass


def add_snapshot_to_checker(checker: CallableT, snapshot: Snapshot) -> None:
    """
    Add the snapshot to the function's checker.

    Use :func:`find_checker` to find the checker.
    If it returns ``None``, decorate it with the checker first using :func:`decorate_with_checker`.
    """
    pass


def add_postcondition_to_checker(checker: CallableT, contract: Contract) -> None:
    """
    Add the postcondition to the function's checker.

    Use :func:`find_checker` to find the checker.
    If it returns ``None``, decorate it with the checker first using :func:`decorate_with_checker`.
    """
    pass


def _find_self(
    param_names: List[str], args: Tuple[Any, ...], kwargs: Dict[str, Any]
) -> Any:
    """Find the instance of ``self`` in the arguments."""
    pass


def _decorate_new_with_invariants(new_func: CallableT) -> CallableT:
    """
    Decorate the ``__new__`` of a class s.t. the invariants are checked on the result.

    This is necessary for optimized classes such as ``namedtuple`` which use ``object.__init__``
    as constructor and do not expect a wrapping around the constructor.
    """
    pass


def _decorate_with_invariants(func: CallableT, cls: ClassT, is_init: bool) -> CallableT:
    """
    Decorate the method ``func`` with invariant checks.

    If the function has been already decorated with invariant checks, the function returns immediately.

    :param func: function to be wrapped
    :param cls: class corresponding to the invariant and ``func``
    :param is_init: True if the ``func`` is __init__
    :return: function wrapped with invariant checks
    """
    pass


class _DummyClass:
    """Represent a dummy class so that we can infer the type of the slot wrapper."""


_SLOT_WRAPPER_TYPE = type(_DummyClass.__init__)  # pylint: disable=invalid-name


def _already_decorated_with_invariants(func: CallableT) -> bool:
    """Check if the function has been already decorated with an invariant check by going through its decorator stack."""
    pass


def add_invariant_checks(cls: ClassT) -> None:
    """Decorate each of the class functions with invariant checks if not already decorated."""
    pass
