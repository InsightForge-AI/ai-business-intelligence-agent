"""
==========================================================
CSV Extractor
==========================================================

Responsibilities
----------------
• Read CSV file
• Validate dataset
• Extract content
• Return standardized response
"""

from pathlib import Path

import pandas as pd


def extract_csv(
    file_path: str
) -> dict:
    """
    Extract CSV document.

    Parameters
    ----------
    file_path : str

    Returns
    -------
    dict
    """

    path = Path(file_path)

    if not path.exists():

        raise FileNotFoundError(

            f"CSV file not found: {path}"

        )

    try:

        dataframe = pd.read_csv(

            path

        )

    except Exception as exc:

        raise RuntimeError(

            f"Unable to read CSV: {exc}"

        ) from exc

    if dataframe.empty:

        raise ValueError(

            "CSV file is empty."

        )

    return {

        "content": dataframe.to_csv(

            index=False

        ),

        "metadata": {

            "file_name": path.name,

            "document_type": "CSV",

            "rows": len(dataframe),

            "columns": len(dataframe.columns),

            "column_names": dataframe.columns.tolist()

        }

    }