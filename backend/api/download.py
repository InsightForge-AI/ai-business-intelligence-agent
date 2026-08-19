"""
==========================================================
Download Document API
==========================================================

Returns original uploaded document file.
"""

import os
import json


from fastapi import APIRouter, HTTPException


from fastapi.responses import FileResponse


from config.settings import METADATA_DIRECTORY
from utils.logger import logger
from utils.validator import validate_document_id



router = APIRouter()





METADATA_PATH = str(METADATA_DIRECTORY)









@router.get(

    "/documents/{document_id}/download"

)

async def download_document(

    document_id: str

):


    try:


        logger.info(

            f"Download request received: {document_id}"

        )

        try:
            document_id = validate_document_id(document_id)
        except ValueError:
            raise HTTPException(status_code=404, detail="Document not found")





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









        file_path = document.get(

            "file_path"

        )





        file_name = (

            document.get("file_name")

            or

            document.get("name")

            or

            "document"

        )









        if not file_path:


            raise HTTPException(

                status_code=404,

                detail="File path not available"

            )









        if not os.path.exists(file_path):


            raise HTTPException(

                status_code=404,

                detail="Uploaded file not found"

            )









        logger.info(

            f"Sending file: {file_name}"

        )









        return FileResponse(


            path=file_path,


            filename=file_name,


            media_type="application/octet-stream"


        )








    except HTTPException:


        raise






    except Exception as error:


        logger.exception(

            f"Download failed: {error}"

        )


        raise HTTPException(

            status_code=500,

            detail="Download failed"

        )