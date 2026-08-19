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
    Validate query.
    """

    return bool(

        query and query.strip()

    )


def validate_content(
    content: str
) -> bool:
    """
    Validate document content.
    """

    return bool(

        content and content.strip()

    )