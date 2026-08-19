"""
==========================================================
Dataset Profiler
==========================================================

Responsibilities
----------------
• Generate dataset statistics
• Identify numeric & categorical columns
• Count missing values
• Provide dataset summary
"""

import pandas as pd


def generate_profile(
    dataframe: pd.DataFrame
) -> dict:
    """
    Generate dataset profile.

    Parameters
    ----------
    dataframe : pandas.DataFrame

    Returns
    -------
    dict
    """

    profile = {

        "rows": len(dataframe),

        "columns": len(dataframe.columns),

        "column_names": list(
            dataframe.columns
        ),

        "numeric_columns": list(

            dataframe.select_dtypes(
                include="number"
            ).columns

        ),

        "categorical_columns": list(

            dataframe.select_dtypes(
                exclude="number"
            ).columns

        ),

        "missing_values":

            dataframe.isnull()

            .sum()

            .to_dict(),

        "data_types":

            dataframe.dtypes

            .astype(str)

            .to_dict()

    }

    return profile