"""
==========================================================
Upload API
==========================================================

Responsibilities
----------------
• Validate uploaded document
• Save uploaded file
• Return file metadata

No document extraction is performed here.
"""

from fastapi import APIRouter
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile


from models.upload_response import UploadResponse


from services.storage_service import save_uploaded_file


from utils.logger import logger





router = APIRouter()







# ==========================================================
# Upload Document
# ==========================================================


@router.post(

    "/upload",

    response_model=UploadResponse

)

async def upload_document(

    file: UploadFile = File(...)

):


    logger.info(

        f"Uploading file: {file.filename}"

    )



    try:


        uploaded_file = await save_uploaded_file(

            file

        )





        logger.info(

            f"Document uploaded successfully: {uploaded_file}"

        )









        return {


            "success": True,


            "message":

                "Document uploaded successfully.",



            "data": {


                "id":

                    uploaded_file.get(

                        "id"

                    ),



                "file_id":

                    uploaded_file.get(

                        "file_id"

                    ),



                "name":

                    uploaded_file.get(

                        "name"

                    ),



                "file_name":

                    uploaded_file.get(

                        "file_name"

                    ),



                "type":

                    uploaded_file.get(

                        "file_type"

                    ),



                "size":

                    uploaded_file.get(

                        "file_size"

                    ),



                "file_path":

                    uploaded_file.get(

                        "file_path"

                    ),



                "status":

                    uploaded_file.get(

                        "status",

                        "Uploaded"

                    )

            }


        }









    except ValueError as exc:



        logger.exception(

            "Invalid upload request."

        )



        raise HTTPException(

            status_code=400,

            detail=str(exc)

        )









    except Exception as exc:



        logger.exception(

            f"Document upload failed: {exc}"

        )



        raise HTTPException(

            status_code=500,

            detail=str(exc)

        )