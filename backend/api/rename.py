"""
==========================================================
Rename Document API
==========================================================

Updates document name in metadata storage.
"""

import os
import json


from fastapi import APIRouter, HTTPException

from pydantic import BaseModel


from utils.logger import logger



router = APIRouter()





METADATA_PATH = "storage/metadata"









class RenameRequest(BaseModel):

    name: str









@router.put(

    "/documents/{document_id}/rename"

)

async def rename_document(

    document_id: str,

    request: RenameRequest

):


    try:


        logger.info(

            f"Rename request received: {document_id}"

        )





        metadata_file = os.path.join(

            METADATA_PATH,

            f"{document_id}.json"

        )





        if not os.path.exists(metadata_file):


            raise HTTPException(

                status_code=404,

                detail="Document not found"

            )









        # -----------------------------------------
        # Read metadata
        # -----------------------------------------

        with open(

            metadata_file,

            "r",

            encoding="utf-8"

        ) as file:


            document = json.load(file)









        old_name = (

            document.get("file_name")

            or

            document.get("name")

        )









        # -----------------------------------------
        # Update name
        # -----------------------------------------

        new_name = request.name.strip()





        if not new_name:


            raise HTTPException(

                status_code=400,

                detail="File name cannot be empty"

            )









        document["file_name"] = new_name


        document["name"] = new_name









        # -----------------------------------------
        # Save metadata
        # -----------------------------------------

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









        logger.info(

            f"Document renamed: {old_name} -> {new_name}"

        )









        return {


            "success": True,


            "message":

                "Document renamed successfully",



            "document": {


                "id": document_id,


                "file_name": new_name


            }


        }








    except HTTPException:


        raise






    except Exception as error:


        logger.exception(

            f"Rename failed: {error}"

        )


        raise HTTPException(

            status_code=500,

            detail="Rename failed"

        )