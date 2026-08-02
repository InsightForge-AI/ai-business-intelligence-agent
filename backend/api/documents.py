"""
==========================================================
Documents API
==========================================================

Responsibilities
----------------
• Get all uploaded documents
• Get single document details
• Return saved AI summary
• Return metadata
• Return AI insights
"""

from fastapi import APIRouter, HTTPException

import os
import json


router = APIRouter()


METADATA_PATH = "storage/metadata"





# ---------------------------------------------------------
# Get All Documents
# ---------------------------------------------------------

@router.get(
    "/documents"
)
async def get_documents():


    documents = []



    if not os.path.exists(METADATA_PATH):

        return {

            "success": True,

            "documents": []

        }





    for filename in os.listdir(METADATA_PATH):


        if not filename.endswith(".json"):

            continue





        file_path = os.path.join(

            METADATA_PATH,

            filename

        )





        try:


            with open(

                file_path,

                "r",

                encoding="utf-8"

            ) as file:


                document = json.load(file)





            documents.append({


                "id":

                    document.get("id")

                    or

                    document.get("file_id"),



                "file_id":

                    document.get("file_id"),



                "name":

                    document.get("name")

                    or

                    document.get("file_name"),



                "type":

                    document.get("file_type"),



                "size":

                    document.get("file_size"),



                "file_path":

                    document.get("file_path"),



                "summary":

                    document.get(

                        "summary",

                        None

                    ),



                "insights":

                    document.get(

                        "insights",

                        None

                    ),



                "metadata":

                    document.get(

                        "metadata",

                        {}

                    ),



                "status":

                    "Processed"

                    if document.get("summary")

                    else "Uploaded",



                "aiReady":

                    bool(

                        document.get("summary")

                    )


            })




        except Exception as error:


            print(

                f"Failed loading {filename}: {error}"

            )





    return {


        "success": True,


        "documents": documents


    }









# ---------------------------------------------------------
# Get Document By ID
# ---------------------------------------------------------

@router.get(

    "/documents/{document_id}"

)

async def get_document_by_id(

    document_id: str

):


    metadata_file = os.path.join(

        METADATA_PATH,

        f"{document_id}.json"

    )



    if not os.path.exists(metadata_file):


        raise HTTPException(

            status_code=404,

            detail="Document not found"

        )





    with open(

        metadata_file,

        "r",

        encoding="utf-8"

    ) as file:


        document = json.load(file)





    return {


        "success": True,


        "document": {


            "id":

                document.get("id")

                or

                document.get("file_id"),



            "file_id":

                document.get("file_id"),



            "name":

                document.get("name")

                or

                document.get("file_name"),



            "type":

                document.get("file_type"),



            "size":

                document.get("file_size"),



            "file_path":

                document.get("file_path"),



            "summary":

                document.get(

                    "summary",

                    None

                ),



            "insights":

                document.get(

                    "insights",

                    None

                ),



            "metadata":

                document.get(

                    "metadata",

                    {}

                )

        }

    }