import pdfplumber
import pandas as pd
import pytesseract

from PIL import Image
from docx import Document


def detect_file_type(filename):

    ext = filename.split(".")[-1].lower()

    return ext

#PDF
def extract_pdf_text(file_path):

    text = ""

    with pdfplumber.open(file_path) as pdf:

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

    if not text.strip():
        return "Scanned PDF detected. OCR for scanned PDFs not supported yet."

    return text

#csv
def extract_csv_text(file_path):

    df = pd.read_csv(file_path)

    return df.to_string(index=False)

#excel
def extract_excel_text(file_path):

    df = pd.read_excel(file_path)

    return df.to_string(index=False)

#docx
def extract_docx_text(file_path):

    doc = Document(file_path)

    text = []

    for para in doc.paragraphs:
        text.append(para.text)

    return "\n".join(text)

#txt
def extract_txt_text(file_path):

    with open(file_path, "r", encoding="utf-8") as file:

        text = file.read()

    return text

#imageOCR
def extract_image_text(file_path):

    image = Image.open(file_path)

    text = pytesseract.image_to_string(image)

    return text


def extract_text(file_path):

    file_type = detect_file_type(file_path)

    if file_type == "pdf":
        return extract_pdf_text(file_path)

    elif file_type == "csv":
        return extract_csv_text(file_path)

    elif file_type in ["xlsx","xls"]:
        return extract_excel_text(file_path)

    elif file_type == "docx":
        return extract_docx_text(file_path)
    
    elif file_type == "txt":
        return extract_txt_text(file_path)


    elif file_type in ["png", "jpg", "jpeg"]:
        return extract_image_text(file_path)

    else:
        return "Unsupported file type"