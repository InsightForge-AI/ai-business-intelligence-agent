"""
==========================================================
Helpers
==========================================================

Common helper functions.
"""


def safe_string(value) -> str:
    """
    Convert any value to string.
    """

    if value is None:

        return ""

    return str(value).strip()


def safe_list(value) -> list:
    """
    Ensure value is a list.
    """

    if value is None:

        return []

    if isinstance(value, list):

        return value

    return [value]