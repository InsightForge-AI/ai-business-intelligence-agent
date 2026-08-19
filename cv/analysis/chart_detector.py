"""
==========================================================
Chart Detector
==========================================================

Responsibilities
----------------
• Detect charts from OCR text
• Identify chart type
• Return detected charts
"""

import re


def detect_charts(
    text: str
) -> list:
    """
    Detect charts mentioned in a document.

    Parameters
    ----------
    text : str

    Returns
    -------
    list
    """

    if not text:

        return []

    charts = []

    text = text.lower()

    # -----------------------------------------------------
    # Bar Chart
    # -----------------------------------------------------

    if re.search(

        r"\b(bar chart|bar graph)\b",

        text

    ):

        charts.append(

            {

                "type": "Bar Chart",

                "detected": True

            }

        )

    # -----------------------------------------------------
    # Line Chart
    # -----------------------------------------------------

    if re.search(

        r"\b(line chart|line graph)\b",

        text

    ):

        charts.append(

            {

                "type": "Line Chart",

                "detected": True

            }

        )

    # -----------------------------------------------------
    # Pie Chart
    # -----------------------------------------------------

    if re.search(

        r"\b(pie chart)\b",

        text

    ):

        charts.append(

            {

                "type": "Pie Chart",

                "detected": True

            }

        )

    # -----------------------------------------------------
    # Area Chart
    # -----------------------------------------------------

    if re.search(

        r"\b(area chart)\b",

        text

    ):

        charts.append(

            {

                "type": "Area Chart",

                "detected": True

            }

        )

    # -----------------------------------------------------
    # Scatter Plot
    # -----------------------------------------------------

    if re.search(

        r"\b(scatter plot|scatter chart)\b",

        text

    ):

        charts.append(

            {

                "type": "Scatter Plot",

                "detected": True

            }

        )

    # -----------------------------------------------------
    # Histogram
    # -----------------------------------------------------

    if re.search(

        r"\b(histogram)\b",

        text

    ):

        charts.append(

            {

                "type": "Histogram",

                "detected": True

            }

        )

    return charts