"""
==========================================================
CV Service
==========================================================

Responsibilities
----------------
• Execute CV pipeline
• Perform OCR
• Classify document
• Extract fields
• Detect tables
• Detect charts
• Enhance results using Llama
• Return standardized response
"""

from analysis.image_loader import load_image
from analysis.preprocessing import preprocess_image
from analysis.ocr import run_ocr
from analysis.classifier import classify_document
from analysis.extractor import extract_fields
from analysis.key_value import extract_key_values
from analysis.table_extractor import extract_tables
from analysis.chart_detector import detect_charts
from analysis.formatter import format_analysis
from analysis.validator import validate_analysis

from llm.llm_service import generate_insights

from models.response import CVResponse

from utils.constants import MODULE_NAME


async def run_analysis(
    query: str,
    content: str,
    metadata: dict
) -> CVResponse:
    """
    Execute Computer Vision analysis.

    Parameters
    ----------
    query : str

    content : str

    metadata : dict

    Returns
    -------
    CVResponse
    """

    # -----------------------------------------------------
    # Load Image
    # -----------------------------------------------------

    image = load_image(

        content

    )

    # -----------------------------------------------------
    # Preprocess Image
    # -----------------------------------------------------

    image = preprocess_image(

        image

    )

    # -----------------------------------------------------
    # OCR
    # -----------------------------------------------------

    extracted_text, confidence = run_ocr(

        image

    )

    # -----------------------------------------------------
    # Document Classification
    # -----------------------------------------------------

    document_type = classify_document(

        extracted_text

    )

    # -----------------------------------------------------
    # Extract Fields
    # -----------------------------------------------------

    fields = extract_fields(

        extracted_text,

        document_type

    )

    # -----------------------------------------------------
    # Key-Value Extraction
    # -----------------------------------------------------

    key_values = extract_key_values(

        extracted_text

    )

    # -----------------------------------------------------
    # Table Extraction
    # -----------------------------------------------------

    tables = extract_tables(

        extracted_text

    )

    # -----------------------------------------------------
    # Chart Detection
    # -----------------------------------------------------

    charts = detect_charts(

        extracted_text

    )

    # -----------------------------------------------------
    # Format Analysis
    # -----------------------------------------------------

    analysis = format_analysis(

        document_type=document_type,

        extracted_text=extracted_text,

        fields=fields,

        key_values=key_values,

        tables=tables,

        charts=charts,

        confidence=confidence

    )

    # -----------------------------------------------------
    # Validate Analysis
    # -----------------------------------------------------

    analysis = validate_analysis(

        analysis

    )

    # -----------------------------------------------------
    # Build LLM Context
    # -----------------------------------------------------

    llm_context = {

        "query": query,

        "metadata": metadata,

        **analysis

    }

    # -----------------------------------------------------
    # Llama Enhancement
    # -----------------------------------------------------

    llm = await generate_insights(

        llm_context

    )

    # -----------------------------------------------------
    # Final Response
    # -----------------------------------------------------

    return CVResponse(

        module=MODULE_NAME,

        success=True,

        document_type=llm.get(

            "document_type",

            analysis["document_type"]

        ),

        extracted_text=llm.get(

            "extracted_text",

            analysis["extracted_text"]

        ),

        fields=llm.get(

            "fields",

            analysis["fields"]

        ),

        tables=llm.get(

            "tables",

            analysis["tables"]

        ),

        charts=llm.get(

            "charts",

            analysis["charts"]

        ),

        confidence=llm.get(

            "confidence",

            analysis["confidence"]

        ),

        message="Computer Vision analysis completed successfully."

    )