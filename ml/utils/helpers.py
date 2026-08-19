"""
==========================================================
Helper Functions
==========================================================
"""

import pandas as pd


def numeric_columns(
    dataframe: pd.DataFrame
):
    """
    Return numeric columns.
    """

    return list(

        dataframe

        .select_dtypes(

            include="number"

        )

        .columns

    )


def categorical_columns(
    dataframe: pd.DataFrame
):
    """
    Return categorical columns.
    """

    return list(

        dataframe

        .select_dtypes(

            exclude="number"

        )

        .columns

    )