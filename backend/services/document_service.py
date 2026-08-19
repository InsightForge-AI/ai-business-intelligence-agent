import json
import os


from services.extraction_service import extract_document
from config.settings import METADATA_DIRECTORY
from utils.validator import validate_document_id



# Anchored to config.settings.BASE_DIR (not the process's CWD, which
# varies depending on how this service is launched -- run.py, a direct
# uvicorn invocation, or a test runner) so metadata is always found in
# the same place regardless of invocation context.
METADATA_PATH = str(METADATA_DIRECTORY)









# ==========================================================
# Get Document
# ==========================================================


async def get_document(

    document_id: str

):

    try:
        document_id = validate_document_id(document_id)
    except ValueError:
        return None

    metadata_file = os.path.join(

        METADATA_PATH,

        f"{document_id}.json"

    )



    if not os.path.exists(metadata_file):

        return None





    with open(

        metadata_file,

        "r",

        encoding="utf-8"

    ) as file:


        document = json.load(file)









    # -----------------------------------------
    # Extract document content
    # -----------------------------------------

    extraction = extract_document(

        document["file_path"]

    )





    document["extracted_text"] = extraction.get(

        "content",

        ""

    )



    document["extraction"] = extraction





    return document













# ==========================================================
# Save Summary
# ==========================================================


async def save_document_summary(

    document_id: str,

    summary: dict

):

    try:
        document_id = validate_document_id(document_id)
    except ValueError:
        return False

    metadata_file = os.path.join(

        METADATA_PATH,

        f"{document_id}.json"

    )



    if not os.path.exists(metadata_file):

        return False





    with open(

        metadata_file,

        "r",

        encoding="utf-8"

    ) as file:


        document = json.load(file)





    document["summary"] = summary





    with open(

        metadata_file,

        "w",

        encoding="utf-8"

    ) as file:


        json.dump(

            document,

            file,

            indent=4,

            ensure_ascii=False

        )





    return True













# ==========================================================
# Save Complete Analysis
# ==========================================================


async def save_document_analysis(

    document_id: str,

    analysis: dict

):

    try:
        document_id = validate_document_id(document_id)
    except ValueError:
        return False

    metadata_file = os.path.join(

        METADATA_PATH,

        f"{document_id}.json"

    )



    if not os.path.exists(metadata_file):

        return False





    with open(

        metadata_file,

        "r",

        encoding="utf-8"

    ) as file:


        document = json.load(file)









    # -----------------------------------------
    # Save AI Output
    # -----------------------------------------


    document["analysis"] = analysis





    # Summary

    if "summary" in analysis:


        document["summary"] = analysis["summary"]









    # Insights

    if "insights" in analysis:


        document["insights"] = analysis["insights"]










    # Update status

    document["status"] = "Processed"









    with open(

        metadata_file,

        "w",

        encoding="utf-8"

    ) as file:


        json.dump(

            document,

            file,

            indent=4,

            ensure_ascii=False

        )







    return True