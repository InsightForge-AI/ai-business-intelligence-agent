import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from parser import analyze_document

sample_text = """
INVOICE
Invoice # 123456
Date 05/01/2024
Total $900
"""

result = analyze_document(sample_text)

print(result)

print("Invoice Number:", result["fields"]["invoice_number"])
print("Amount:", result["fields"]["amount"])
print("Test Passed")