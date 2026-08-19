"""
==========================================================
Text Loader
==========================================================

Responsibilities
----------------
• Load extracted document text
• Normalize input
• Remove empty content
"""



def load_text(
    content: str
) -> str:
    """
    Load document text.

    Parameters
    ----------
    content : str

    Returns
    -------
    str
    """

    if content is None:

        return ""

    if not isinstance(content, str):

        content = str(content)

    content = content.strip()

    return content