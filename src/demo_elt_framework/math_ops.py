from __future__ import annotations

from typing import Union

from .exceptions import DivisionByZeroError, ValidationError

Number = Union[int, float]


def _ensure_number(x: object, name: str) -> Number:
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        raise ValidationError(f"{name} must be int or float; got {type(x).__name__}")
    return x


def add(a: Number, b: Number) -> Number:
    """Return a + b."""
    a = _ensure_number(a, "a")
    b = _ensure_number(b, "b")
    return a + b


def subtract(a: Number, b: Number) -> Number:
    """Return a - b."""
    a = _ensure_number(a, "a")
    b = _ensure_number(b, "b")
    return a - b


def divide(a: Number, b: Number, *, on_zero: str = "raise") -> float:
    """Return a / b.

    Parameters
    ----------
    on_zero:
        Behavior when b == 0.
        - "raise": raise DivisionByZeroError
        - "inf": return +inf or -inf depending on sign of a
        - "nan": return nan
    """
    a = float(_ensure_number(a, "a"))
    b = float(_ensure_number(b, "b"))

    if b == 0.0:
        if on_zero == "raise":
            raise DivisionByZeroError("division by zero")
        if on_zero == "inf":
            if a == 0.0:
                return float("nan")
            return float("inf") if a > 0 else float("-inf")
        if on_zero == "nan":
            return float("nan")
        raise ValidationError('on_zero must be one of: "raise", "inf", "nan"')

    return a / b
