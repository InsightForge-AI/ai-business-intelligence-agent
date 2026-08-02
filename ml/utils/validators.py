"""
==========================================================
Validators
==========================================================
"""

import pandas as pd


def validate_dataframe(
    dataframe: pd.DataFrame
):
    """
    Validate DataFrame.
    """

    if dataframe.empty:

        raise ValueError(
            "Dataset is empty."
        )

    if len(dataframe.columns) == 0:

        raise ValueError(
            "No columns found."
        )

    return True