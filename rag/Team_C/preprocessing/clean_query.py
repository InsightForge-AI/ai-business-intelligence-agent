#preprocessing the text cleaning
def clean_query(query: str):

    query = query.lower()

    tokens = query.split()

    return tokens