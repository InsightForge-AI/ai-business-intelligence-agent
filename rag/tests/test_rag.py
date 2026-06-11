from ingest import build_document_index
from retriever import retrieve_context


def test_refund_policy():

    document = """
    Customers may request refunds
    within 7 days of purchase.
    """

    index, chunks = (
        build_document_index(
            document
        )
    )

    result = (
        retrieve_context(
            "What is refund policy?",
            index,
            chunks
        )
    )

    assert (
        len(
            result[
                "retrieved_chunks"
            ]
        ) > 0
    )


def test_unknown_question():

    document = """
    Customers may request refunds
    within 7 days.
    """

    index, chunks = (
        build_document_index(
            document
        )
    )

    result = (
        retrieve_context(
            "Who is CEO?",
            index,
            chunks
        )
    )

    assert result is not None