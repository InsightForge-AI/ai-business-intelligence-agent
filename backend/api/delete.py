"""
==========================================================
Delete Document API
==========================================================

Deletes uploaded document,
metadata,
and generated AI data.
"""

import os
import json


from fastapi import APIRouter, HTTPException


from config.settings import METADATA_DIRECTORY, UPLOAD_DIRECTORY
from utils.logger import logger
from utils.validator import validate_document_id



router = APIRouter()





METADATA_PATH = str(METADATA_DIRECTORY)

UPLOAD_PATH = str(UPLOAD_DIRECTORY)









@router.delete(

    "/documents/{document_id}"

)

async def delete_document(

    document_id: str

):


    try:


        logger.info(

            f"Delete request received: {document_id}"

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









        # -----------------------------------------
        # Delete uploaded file
        # -----------------------------------------

        if file_path and os.path.exists(file_path):


            os.remove(

                file_path

            )


            logger.info(

                f"Deleted file: {file_path}"

            )









        # -----------------------------------------
        # Delete metadata
        # -----------------------------------------

        if os.path.exists(metadata_file):


            os.remove(

                metadata_file

            )


            logger.info(

                f"Deleted metadata: {metadata_file}"

            )









        # -----------------------------------------
        # Optional AI data cleanup
        # -----------------------------------------

        ai_files = [


            f"storage/summaries/{document_id}.json",


            f"storage/insights/{document_id}.json",


            f"storage/vector/{document_id}"


        ]





        for path in ai_files:


            if os.path.exists(path):


                if os.path.isdir(path):


                    import shutil


                    shutil.rmtree(path)


                else:


                    os.remove(path)









        return {


            "success": True,


            "message":

                "Document deleted successfully",



            "document_id":

                document_id


        }








    except HTTPException:


        raise






    except Exception as error:


        logger.exception(

            f"Delete failed: {error}"

        )



        raise HTTPException(

            status_code=500,

            detail="Delete failed"

        )