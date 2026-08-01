"""
==========================================================
Document Classifier
==========================================================

Responsibilities
----------------
• Classify document type
• Detect invoices
• Detect receipts
• Detect reports
• Detect contracts
• Detect bank statements
"""

import re

from utils.constants import DOCUMENT_TYPES


def classify_document(
    text: str
) -> str:
    """
    Classify document based on extracted text.

    Parameters
    ----------
    text : str

    Returns
    -------
    str
    """

    if not text:

        return "Unknown"

    text = text.lower()

    # -----------------------------------------------------
    # Invoice
    # -----------------------------------------------------

    if re.search(

        r"\binvoice\b",

        text

    ):

        return "Invoice"

    # -----------------------------------------------------
    # Receipt
    # -----------------------------------------------------

    if re.search(

        r"\breceipt\b",

        text

    ):

        return "Receipt"

    # -----------------------------------------------------
    # Bank Statement
    # -----------------------------------------------------

    if (

        "bank statement" in text

        or "account number" in text

        or "available balance" in text

        or "opening balance" in text

        or "closing balance" in text

    ):

        return "Bank Statement"

    # -----------------------------------------------------
    # Contract
    # -----------------------------------------------------

    if (

        "agreement" in text

        or "contract" in text

        or "party" in text

        or "terms and conditions" in text

    ):

        return "Contract"

    # -----------------------------------------------------
    # Resume
    # -----------------------------------------------------

    if (

        "education" in text

        and "experience" in text

        and "skills" in text

    ):

        return "Resume"

    # -----------------------------------------------------
    # Medical Report
    # -----------------------------------------------------

    if (

        "patient" in text

        or "diagnosis" in text

        or "hospital" in text

        or "doctor" in text

        or "prescription" in text

    ):

        return "Medical Report"

    # -----------------------------------------------------
    # Passport
    # -----------------------------------------------------

    if (

        "passport" in text

        or "nationality" in text

        or "date of birth" in text

    ):

        return "Passport"

    # -----------------------------------------------------
    # ID Card
    # -----------------------------------------------------

    if (

        "identity card" in text

        or "aadhaar" in text

        or "driving licence" in text

        or "driving license" in text

    ):

        return "ID Card"

    # -----------------------------------------------------
    # Report
    # -----------------------------------------------------

    if (

        "report" in text

        or "summary" in text

        or "analysis" in text

        or "introduction" in text

        or "conclusion" in text

    ):

        return "Report"

    # -----------------------------------------------------
    # Unknown
    # -----------------------------------------------------

    return "Unknown"