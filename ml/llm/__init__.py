"""
formatter.py

Utility functions for formatting numeric values
into Indian currency notation.

Examples
--------
125           -> ₹125.00
5_400         -> ₹5.40 K
7_50_000      -> ₹7.50 Lakh
3_45_00_000   -> ₹3.45 Cr
"""


def format_indian_currency(value: float | int | None) -> str:
    """
    Format a numeric value into Indian currency notation.

    Parameters
    ----------
    value : float | int | None
        Numeric value.

    Returns
    -------
    str
        Formatted currency string.
    """

    if value is None:
        return "₹0.00"

    try:
        value = float(value)
    except (TypeError, ValueError):
        return "₹0.00"

    sign = "-" if value < 0 else ""
    value = abs(value)

    if value >= 1_00_00_000:
        formatted = f"{value / 1_00_00_000:.2f} Cr"

    elif value >= 1_00_000:
        formatted = f"{value / 1_00_000:.2f} Lakh"

    elif value >= 1_000:
        formatted = f"{value / 1_000:.2f} K"

    else:
        formatted = f"{value:.2f}"

    return f"{sign}₹{formatted}"