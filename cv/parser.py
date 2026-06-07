import re
import json


def clean_text(ocr_text: str) -> str:
    """
    INPUT  : raw OCR text string from Narayani
    OUTPUT : cleaned text ready for classification and extraction
    """
    text = re.sub(r'\n{3,}', '\n\n', ocr_text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()


# ─────────────────────────────────────────────
# STEP 2: DOCUMENT TYPE CLASSIFICATION
# ─────────────────────────────────────────────
def classify_document(text: str) -> str:
    """
    INPUT  : cleaned OCR text string
    OUTPUT : "invoice" | "receipt" | "unknown"
    """
    text_lower = text.lower()

    invoice_keywords = [
        "invoice", "invoice no", "invoice number",
        "bill to", "subtotal", "tax", "total due",
        "payment terms", "due date", "total"
    ]

    receipt_keywords = [
        "receipt", "thank you for your purchase",
        "transaction id", "payment received",
        "cashier", "change due", "cash", "card"
    ]

    invoice_score = sum(1 for kw in invoice_keywords if kw in text_lower)
    receipt_score = sum(1 for kw in receipt_keywords if kw in text_lower)

    if invoice_score == 0 and receipt_score == 0:
        return "unknown"

    return "invoice" if invoice_score >= receipt_score else "receipt"


# ─────────────────────────────────────────────
# STEP 3: FIELD EXTRACTION USING REGEX/PARSING
# Extract: invoice number, date, amount, names
# ─────────────────────────────────────────────
def extract_fields(text: str) -> dict:
    """
    INPUT  : cleaned OCR text string
    OUTPUT : dict with invoice_number, date, amount,
             customer_name, vendor_name
    """
    fields = {}

    text = re.sub(
        r'(?<=\d)[FIl](?=\d)',
        '/',
        text
    )

    # Invoice Number
    inv = re.search(
        r'Invoice\s*(?:#|No|Number)?\s*[:\-]?\s*([0-9]{3,})',
        text,
        re.IGNORECASE
    )

    fields["invoice_number"] = (
        inv.group(1)
        if inv else None
    )

    # Date
    date = re.search(
        r'\b(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}'
        r'|\d{4}[\/\-]\d{2}[\/\-]\d{2}'
        r'|\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
        r'[a-z]*\s+\d{4})\b',
        text,
        re.IGNORECASE
    )
    fields["date"] = date.group(0) if date else None

    # Amount / Total
    amount_matches = re.findall(
        r'(?:total|tolal|toel|grand total)[^\d$₹]*[\$₹&]?\s*([\d,]+(?:\.\d{2})?)',
        text,
        re.IGNORECASE
    )
    print("AMOUNT MATCHES =", amount_matches)

    fields["amount"] = (
        amount_matches[-1].replace(",", "")
        if amount_matches else None
    )

    # Vendor / Company Name
    vendor = re.search(
        r'(?:from|issued by|company|vendor)[:\s]+'
        r'([A-Z][a-zA-Z\s&\.]+?)(?:\n|,|$)',
        text,
        re.IGNORECASE
    )

    fields["vendor_name"] = vendor.group(1).strip() if vendor else None

    return fields


def analyze_document(ocr_text: str) -> dict:
    """
    INPUT  : raw OCR text from Narayani's run_ocr()
    OUTPUT : final JSON result → API response
    """

    # Basic Error Handling
    if not ocr_text or not ocr_text.strip():
        return {
            "status": "error",
            "message": "OCR text is empty.",
            "document_type": "unknown",
            "extracted_fields": {},
            "missing_fields": [],
            "summary": None
        }

    cleaned = clean_text(ocr_text)

    doc_type = classify_document(cleaned)

    fields = extract_fields(cleaned)

    # Missing Fields
    missing_fields = [
        key for key, value in fields.items()
        if value is None
    ]

    # Summary Field
    summary = (
        f"Document classified as {doc_type}. "
        f"Invoice Number: {fields.get('invoice_number') or 'Not Found'}, "
        f"Date: {fields.get('date') or 'Not Found'}, "
        f"Amount: {fields.get('amount') or 'Not Found'}."
    )

    result = {
        "document_type": doc_type,
        "invoice_number": fields.get("invoice_number"),
        "date": fields.get("date"),
        "amount": fields.get("amount")
    }

    return result


# ─────────────────────────────────────────────
# STANDALONE TEST
# Run: python document_classifier.py
# ─────────────────────────────────────────────
if __name__ == "__main__":

    sample_ocr_text = """
    INVOICE
    Company Name
    Street Address
    City ST ZIP
    Phone 000 000-0000
    Invoice # 123456
    Date 5/1/2014
    Bill To Name
    Company Name
    Street Address
    City ST ZIP
    Phone
    Email Address
    Description Amount
    Service Fee 200.00
    Labor 5 hours at 75/hr 375.00
    New client discount -50.00
    Tax 4.25 after discount 26.56
    Thank you for your business
    Total $ 551.56
    """

    print("=" * 55)
    print("  SPRINT 5")
    print("=" * 55)

    result = analyze_document(sample_ocr_text)

    print("\nOUTPUT (Final JSON sent to API):")
    print("─" * 55)
    print(json.dumps(result, indent=2))
    print("─" * 55)

    print("\n[✔] Task complete → ready for Team Lead integration")