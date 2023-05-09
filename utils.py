"""Utilities module."""

from config import STATUS_CHOICES


def status_full_name(short_name: str) -> str:
    """Get full readable string for order status."""

    try:
        result = STATUS_CHOICES[str(short_name)]
    except:
        return short_name

    return result
