"""Decorator to mark a function as not completed."""

import functools
import warnings


def not_completed(func):
    """Decorator to mark a function as not completed."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        warnings.warn(f"'{func.__name__}' is marked as not completed", UserWarning)

        return func(*args, **kwargs)

    return wrapper
