from fastapi import APIRouter, HTTPException


from services.summary_service import generate_document_summary


from services.document_service import (
    get_document,
    save_document_summary
)



router = APIRouter()





@router.post(
    "/documents/{document_id}/summary"
)
async def create_summary(document_id: str):


    document = await get_document(

        document_id

    )



    if not document:


        raise HTTPException(

            status_code=404,

            detail="Document not found"

        )







    result = await generate_document_summary(

        document

    )







    # -----------------------------------------
    # Extract Summary + Insights
    # -----------------------------------------

    summary = result.get(

        "summary",

        {}

    )



    insights = result.get(

        "insights",

        {}

    )







    # -----------------------------------------
    # Save generated AI results
    # -----------------------------------------

    await save_document_summary(

        document_id,

        {

            "summary": summary,

            "insights": insights

        }

    )







    return {


        "success": True,


        "document_id": document_id,


        "summary": summary,


        "insights": insights


    }