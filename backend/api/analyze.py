"""
==========================================================
Analyze API
==========================================================

Responsibilities
----------------
• Receive document analysis request
• Validate document
• Trigger orchestration
• Save AI results
• Return analysis response
"""

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Query


from services.orchestration_service import run_analysis

from services.document_service import (
    get_document,
    save_document_analysis
)


from utils.logger import logger



router = APIRouter()









# ==========================================================
# Analyze Document
# ==========================================================


@router.post(
    "/analyze/{document_id}"
)
async def analyze_document(

    document_id: str,

    query: str = Query(

        default="Analyze this document and generate insights"

    )

):


    logger.info(

        f"Analysis started: {document_id}"

    )



    try:




        # -----------------------------------------
        # Get Document
        # -----------------------------------------

        document = await get_document(

            document_id

        )





        if not document:


            logger.warning(

                f"Document not found: {document_id}"

            )


            raise HTTPException(

                status_code=404,

                detail="Document not found"

            )









        # -----------------------------------------
        # Run AI Pipeline
        # -----------------------------------------

        result = await run_analysis(

            file_id=document_id,

            query=query

        )









        # -----------------------------------------
        # Save Analysis Result
        # -----------------------------------------

        saved = await save_document_analysis(

            document_id,

            result

        )





        if not saved:


            logger.warning(

                "Analysis generated but save failed"

            )









        logger.info(

            "Analysis completed successfully"

        )









        return {


            "success": True,


            "message":

                "Analysis completed successfully.",



            "document_id":

                document_id,



            "summary":

                result.get(

                    "summary",

                    {}

                ),



            "insights":

                result.get(

                    "insights",

                    {}

                ),



            "data":

                result


        }









    except HTTPException:

        raise









    except FileNotFoundError as exc:


        logger.exception(

            "File missing"

        )


        raise HTTPException(

            status_code=404,

            detail=str(exc)

        )









    except Exception as exc:


        logger.exception(

            f"Analysis failed: {exc}"

        )


        raise HTTPException(

            status_code=500,

            detail="Analysis failed"

        )