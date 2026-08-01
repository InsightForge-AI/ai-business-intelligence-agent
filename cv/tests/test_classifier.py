"""
==========================================================
Document Classifier Tests
==========================================================

Tests document classification.
"""

from analysis.classifier import classify_document


def test_invoice():
    """
    Test Invoice.
    """

    text = """

    Invoice Number : INV-1001

    Total : $5200

    """

    assert classify_document(

        text

    ) == "Invoice"


def test_receipt():
    """
    Test Receipt.
    """

    text = """

    Receipt Number : REC-101

    Amount : $250

    """

    assert classify_document(

        text

    ) == "Receipt"


def test_report():
    """
    Test Report.
    """

    text = """

    Annual Report

    Executive Summary

    Business Analysis

    Conclusion

    """

    assert classify_document(

        text

    ) == "Report"


def test_contract():
    """
    Test Contract.
    """

    text = """

    Service Agreement

    Terms and Conditions

    """

    assert classify_document(

        text

    ) == "Contract"


def test_bank_statement():
    """
    Test Bank Statement.
    """

    text = """

    Bank Statement

    Account Number : 123456789

    Opening Balance : $5000

    Closing Balance : $7000

    """

    assert classify_document(

        text

    ) == "Bank Statement"


def test_resume():
    """
    Test Resume.
    """

    text = """

    Education

    Experience

    Skills

    """

    assert classify_document(

        text

    ) == "Resume"


def test_medical_report():
    """
    Test Medical Report.
    """

    text = """

    Patient Name

    Diagnosis

    Doctor

    Hospital

    """

    assert classify_document(

        text

    ) == "Medical Report"


def test_passport():
    """
    Test Passport.
    """

    text = """

    Passport

    Nationality

    Date of Birth

    """

    assert classify_document(

        text

    ) == "Passport"


def test_id_card():
    """
    Test ID Card.
    """

    text = """

    Aadhaar

    Identity Card

    """

    assert classify_document(

        text

    ) == "ID Card"


def test_unknown():
    """
    Test Unknown.
    """

    text = """

    Hello World

    Random Text

    """

    assert classify_document(

        text

    ) == "Unknown"