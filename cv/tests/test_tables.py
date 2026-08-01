"""
==========================================================
Table Extraction Tests
==========================================================

Tests table extraction.
"""

from analysis.table_extractor import extract_tables


def test_pipe_table():
    """
    Test pipe-separated table.
    """

    text = """
    | Item | Qty | Price |
    | Laptop | 2 | $1200 |
    | Mouse | 5 | $20 |
    """

    tables = extract_tables(

        text

    )

    assert len(

        tables

    ) == 1

    assert tables[0][0] == [

        "Item",

        "Qty",

        "Price"

    ]


def test_space_table():
    """
    Test multi-space table.
    """

    text = """
    Item      Qty      Price
    Laptop    2        $1200
    Mouse     5        $20
    """

    tables = extract_tables(

        text

    )

    assert len(

        tables

    ) == 1

    assert tables[0][0] == [

        "Item",

        "Qty",

        "Price"

    ]


def test_multiple_tables():
    """
    Test multiple tables.
    """

    text = """
    Item      Qty

    Laptop    2

    Mouse     5


    Name      Marks

    John      95

    Alice     89
    """

    tables = extract_tables(

        text

    )

    assert len(

        tables

    ) == 2


def test_empty_table():
    """
    Test empty input.
    """

    tables = extract_tables(

        ""

    )

    assert tables == []