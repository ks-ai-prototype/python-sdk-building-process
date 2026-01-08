from __future__ import annotations


class DemoELTError(Exception):
    """Base exception for demo-elt-framework."""


class ValidationError(DemoELTError):
    """Raised when user input is invalid."""


class DivisionByZeroError(DemoELTError):
    """Raised when division by zero occurs and is configured to error."""


class TransformError(DemoELTError):
    """Raised when a transformation fails."""
