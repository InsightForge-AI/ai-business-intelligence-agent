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

    consecutive_blank_lines = 0

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        if not line:

            consecutive_blank_lines += 1

            # A single blank line is treated as row-spacing noise (common
            # in real OCR output, where line-height variance can insert
            # a blank line between table rows) rather than the end of
            # the table. Two or more consecutive blank lines is treated
            # as an actual section break.
            if (
                current_table
                and consecutive_blank_lines >= 2
            ):

                tables.append(

                    current_table

                )

                current_table = []

            continue

        consecutive_blank_lines = 0

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