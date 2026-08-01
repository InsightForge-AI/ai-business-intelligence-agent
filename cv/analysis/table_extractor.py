"""
==========================================================
Table Extractor
==========================================================

Responsibilities
----------------
• Detect tables
• Extract rows
• Return structured table data
"""

import re


def extract_tables(
    text: str
) -> list:
    """
    Extract tables from OCR text.

    Parameters
    ----------
    text : str

    Returns
    -------
    list
    """

    if not text:

        return []

    tables = []

    current_table = []

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        if not line:

            if current_table:

                tables.append(

                    current_table

                )

                current_table = []

            continue

        # -------------------------------------------------
        # Pipe-Separated Tables
        # -------------------------------------------------

        if "|" in line:

            row = [

                column.strip()

                for column in line.split(

                    "|"

                )

                if column.strip()

            ]

            current_table.append(

                row

            )

            continue

        # -------------------------------------------------
        # Multi-space Columns
        # -------------------------------------------------

        columns = re.split(

            r"\s{2,}",

            line

        )

        if len(columns) >= 2:

            current_table.append(

                columns

            )

        else:

            if current_table:

                tables.append(

                    current_table

                )

                current_table = []

    if current_table:

        tables.append(

            current_table

        )

    return tables