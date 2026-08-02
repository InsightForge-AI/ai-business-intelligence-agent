"""
==========================================================
Validators
==========================================================

Validation utilities.
"""


def validate_query(
    query: str
) -> bool:
    """
    Validate user query.
    """

    return bool(

        query and query.strip()

    )


def validate_content(
    content: str
) -> bool:
    """
    Validate extracted content.
    """

    return bool(

        content and content.strip()

    )