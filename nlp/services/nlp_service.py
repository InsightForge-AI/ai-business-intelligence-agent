"""
==========================================================
NLP Service
==========================================================

Responsibilities
----------------
• Execute NLP pipeline
• Perform deterministic NLP analysis
• Enhance results using Mistral
• Return standardized response
"""

from analysis.loader import load_text
from analysis.preprocessing import preprocess_text
from analysis.summarizer import generate_summary
from analysis.sentiment import analyze_sentiment
from analysis.keywords import extract_keywords
from analysis.ner import extract_entities
from analysis.topics import detect_topics
from analysis.recommendations import generate_recommendations
from analysis.formatter import format_analysis

from llm.llm_service import generate_insights

from models.response import NLPResponse


async def run_analysis(
    query: str,
    content: str,
    metadata: dict
) -> NLPResponse:
    """
    Execute NLP analysis.

    Parameters
    ----------
    query : str

    content : str

    metadata : dict

    Returns
    -------
    NLPResponse
    """

    # -----------------------------------------------------
    # Load Text
    # -----------------------------------------------------

    text = load_text(

        content

    )

    # -----------------------------------------------------
    # Preprocess
    # -----------------------------------------------------

    text = preprocess_text(

        text

    )

    # -----------------------------------------------------
    # Traditional NLP
    # -----------------------------------------------------

    summary = generate_summary(

        text

    )

    keywords = extract_keywords(

        text

    )

    entities = extract_entities(

        text

    )

    sentiment = analyze_sentiment(

        text

    )

    topics = detect_topics(

        keywords

    )

    recommendations = generate_recommendations(

        sentiment,

        topics

    )

    # -----------------------------------------------------
    # Format Analysis
    # -----------------------------------------------------

    analysis = format_analysis(

        summary=summary,

        keywords=keywords,

        entities=entities,

        sentiment=sentiment,

        topics=topics,

        recommendations=recommendations

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
    # Mistral Enhancement
    # -----------------------------------------------------

    llm = await generate_insights(

        llm_context

    )

    # -----------------------------------------------------
    # Final Response
    # -----------------------------------------------------

    return NLPResponse(

        module="nlp",

        success=True,

        summary=llm.get(

            "summary",

            summary

        ),

        keywords=llm.get(

            "keywords",

            keywords

        ),

        entities=llm.get(

            "entities",

            entities

        ),

        sentiment=llm.get(

            "sentiment",

            sentiment

        ),

        topics=llm.get(

            "topics",

            topics

        ),

        recommendations=llm.get(

            "recommendations",

            recommendations

        ),

        message="NLP analysis completed successfully."

    )