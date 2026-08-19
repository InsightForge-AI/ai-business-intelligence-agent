"""
==========================================================
Field Extractor
==========================================================

Responsibilities
----------------
• Extract structured fields
• Invoice number
• Date
• Vendor
• Customer
• Amount
"""

import re


def extract_fields(
    text: str,
    document_type: str
) -> dict:
    """
    Extract important fields.

    Parameters
    ----------
    text : str

    document_type : str

    Returns
    -------
    dict
    """

    if not text:

        return {}

    fields = {}

    # -----------------------------------------------------
    # Invoice
    # -----------------------------------------------------

    if document_type == "Invoice":

        invoice = re.search(

            r"(?:invoice\s*(?:number|no|#)?[:\s]*)"
            r"([A-Za-z0-9\-\/]+)",

            text,

            re.IGNORECASE

        )

        if invoice:

            fields["invoice_number"] = invoice.group(1)

    # -----------------------------------------------------
    # Receipt
    # -----------------------------------------------------

    if document_type == "Receipt":

        receipt = re.search(

            r"(?:receipt\s*(?:number|no|#)?[:\s]*)"
            r"([A-Za-z0-9\-\/]+)",

            text,

            re.IGNORECASE

        )

        if receipt:

            fields["receipt_number"] = receipt.group(1)

    # -----------------------------------------------------
    # Date
    # -----------------------------------------------------

    date = re.search(

        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",

        text

    )

    if date:

        fields["date"] = date.group()

    # -----------------------------------------------------
    # Amount
    # -----------------------------------------------------

    amount = re.search(

        r"(?:total|amount|grand total)"
        r"\s*[:\-]?\s*"
        r"(\$?\s?[\d,]+(?:\.\d{2})?)",

        text,

        re.IGNORECASE

    )

    if amount:

        fields["amount"] = amount.group(1)

    # -----------------------------------------------------
    # Vendor
    # -----------------------------------------------------

    vendor = re.search(

        r"(?:vendor|supplier|seller)"
        r"\s*[:\-]?\s*(.+)",

        text,

        re.IGNORECASE

    )

    if vendor:

        fields["vendor"] = vendor.group(1).strip()

    # -----------------------------------------------------
    # Customer
    # -----------------------------------------------------

    customer = re.search(

        r"(?:customer|bill to|client)"
        r"\s*[:\-]?\s*(.+)",

        text,

        re.IGNORECASE

    )

    if customer:

        fields["customer"] = customer.group(1).strip()

    return fields