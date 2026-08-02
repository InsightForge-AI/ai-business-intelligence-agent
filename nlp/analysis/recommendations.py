"""
==========================================================
Recommendation Engine
==========================================================

Responsibilities
----------------
• Generate actionable recommendations
• Use sentiment and detected topics
• Return business recommendations
"""

from utils.constants import MAX_RECOMMENDATIONS


def generate_recommendations(
    sentiment: str,
    topics: list[str]
) -> list[str]:
    """
    Generate recommendations.

    Parameters
    ----------
    sentiment : str

    topics : list[str]

    Returns
    -------
    list[str]
    """

    recommendations = []

    # -----------------------------------------------------
    # Sentiment Based
    # -----------------------------------------------------

    if sentiment == "Negative":

        recommendations.append(

            "Investigate the factors contributing to negative sentiment and develop corrective actions."

        )

    elif sentiment == "Neutral":

        recommendations.append(

            "Monitor business performance to identify opportunities for improvement."

        )

    elif sentiment == "Positive":

        recommendations.append(

            "Maintain current strategies while exploring opportunities for future growth."

        )

    # -----------------------------------------------------
    # Topic Based
    # -----------------------------------------------------

    for topic in topics:

        if topic == "Finance":

            recommendations.append(

                "Review financial performance and optimize revenue while controlling operational costs."

            )

        elif topic == "Business":

            recommendations.append(

                "Strengthen customer engagement and expand market opportunities."

            )

        elif topic == "Operations":

            recommendations.append(

                "Improve operational efficiency by optimizing supply chain and inventory management."

            )

        elif topic == "Human Resources":

            recommendations.append(

                "Invest in employee development and workforce planning."

            )

        elif topic == "Technology":

            recommendations.append(

                "Accelerate digital transformation and adopt AI-driven automation where appropriate."

            )

    # -----------------------------------------------------
    # Remove Duplicates
    # -----------------------------------------------------

    recommendations = list(

        dict.fromkeys(recommendations)

    )

    return recommendations[:MAX_RECOMMENDATIONS]