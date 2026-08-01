"""
========================================
Dashboard API
========================================

Responsibilities
----------------
• Load dashboard data
• Return active document
• Return workspace statistics
• Return intelligence data
"""

from fastapi import APIRouter
from fastapi import HTTPException


from services.dashboard_service import get_dashboard


from utils.logger import logger





router = APIRouter(

    prefix="/dashboard",

    tags=["Dashboard"]

)









# ==========================================================
# Dashboard
# ==========================================================


@router.get("")

async def dashboard():


    try:


        logger.info(

            "Loading dashboard data..."

        )





        response = await get_dashboard()





        logger.info(

            "Dashboard loaded successfully."

        )





        return {


            "success":True,


            "message":

                "Dashboard loaded successfully.",



            "data":response


        }









    except Exception as error:



        logger.exception(

            "Dashboard loading failed."

        )



        raise HTTPException(

            status_code=500,

            detail=str(error)

        )