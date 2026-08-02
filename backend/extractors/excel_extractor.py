"""
==========================================================
Excel Extractor
==========================================================

Responsibilities
----------------
• Read Excel file
• Validate dataset
• Extract structured content
• Return standardized response

No AI logic.
"""

from pathlib import Path

import pandas as pd


def extract_excel(file_path: str) -> dict:
    """
    Extract Excel document.

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
            f"Excel file not found: {path}"
        )

    try:
        dataframe = pd.read_excel(path)

    except Exception as exc:
        raise RuntimeError(
            f"Unable to read Excel file: {exc}"
        ) from exc

    if dataframe.empty:
        raise ValueError(
            "Excel file is empty."
        )

    # -----------------------------------------
    # Clean Dataset
    # -----------------------------------------

    dataframe = dataframe.where(
        pd.notnull(dataframe),
        None
    )

    # -----------------------------------------
    # Convert to Structured Records
    # -----------------------------------------

    records = dataframe.to_dict(
        orient="records"
    )

    return {

        "content": records,

        "tables": [],

        "images": [],

        "metadata": {

            "file_name": path.name,

            "document_type": "Excel",

            "rows": len(dataframe),

            "columns": len(dataframe.columns),

            "column_names": dataframe.columns.tolist(),

            "sheet_count": 1

        }

    }