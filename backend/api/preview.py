from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from services.document_service import get_document


router = APIRouter()



@router.get("/documents/{document_id}/preview")
async def preview_document(document_id: str):


    document = await get_document(

        document_id

    )


    if not document:

        raise HTTPException(

            status_code=404,

            detail="Document not found"

        )



    file_path = document.get(

        "file_path"

    )


    if not file_path:

        raise HTTPException(

            status_code=404,

            detail="File path missing"

        )



    return FileResponse(

        path=file_path,

        media_type="application/pdf"

    )