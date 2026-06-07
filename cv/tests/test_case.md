Test Case 1
Input: Invoice Image
Expected:
- document_type = invoice
- invoice_number extracted
- amount extracted

Result: Pass

--------------------------------

Test Case 2
Input: Receipt Image
Expected:
- document_type = receipt
- amount extracted

Result: Pass

--------------------------------

Test Case 3
Input: Blurry Image
Expected:
- OCR error handling

Result: Pass