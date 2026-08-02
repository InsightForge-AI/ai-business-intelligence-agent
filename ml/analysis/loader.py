"""
==========================================================
ML Data Loader
==========================================================

Responsibilities
----------------
• Receive structured data from Backend
• Convert data into Pandas DataFrame
• Validate dataset
• Return DataFrame
"""

import pandas as pd


def load_data(content):
    """
    Convert Backend structured content
    into a Pandas DataFrame.

    Parameters
    ----------
    content : list | dict

    Returns
    -------
    pandas.DataFrame
    """

    if content is None:

        raise ValueError(
            "No data received from Backend."
        )

    # -----------------------------------------
    # Already a DataFrame
    # -----------------------------------------

    if isinstance(content, pd.DataFrame):

        dataframe = content

    # -----------------------------------------
    # List of Records
    # -----------------------------------------

    elif isinstance(content, list):

        dataframe = pd.DataFrame(content)

    # -----------------------------------------
    # Dictionary
    # -----------------------------------------

    elif isinstance(content, dict):

        dataframe = pd.DataFrame([content])

    else:

        raise TypeError(
            "Unsupported content format."
        )

    # -----------------------------------------
    # Validate Dataset
    # -----------------------------------------

    if dataframe.empty:

        raise ValueError(
            "Dataset is empty."
        )

    return dataframe