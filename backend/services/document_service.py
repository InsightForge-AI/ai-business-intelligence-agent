import json
import os


from services.extraction_service import extract_document



METADATA_PATH = "storage/metadata"









# ==========================================================
# Get Document
# ==========================================================


async def get_document(

    document_id: str

):


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