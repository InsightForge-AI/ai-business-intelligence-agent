"""
==========================================================
Agent Service
==========================================================

Backend client for Agent service.

Responsibilities
----------------
• Call Agent API
• Normalize routing decision
"""

import httpx


from config.endpoints import AGENT_API

from utils.logger import logger







def normalize_agent_response(response: dict):


    return {


        "intent":

            response.get(

                "intent",

                ""

            ),



        "selected_modules":

            response.get(

                "selected_modules",

                []

            ),



        "execution_order":

            response.get(

                "execution_order",

                []

            ),



        "reason":

            response.get(

                "reason",

                ""

            )


    }









async def run_agent(

    query:str,

    metadata:dict

)->dict:


    payload = {


        "query":

            query,



        "metadata":

            metadata


    }





    logger.info(

        "Calling Agent Service..."

    )


















    try:



        async with httpx.AsyncClient(

            timeout=120

        ) as client:



            response = await client.post(


                f"{AGENT_API}/agent/analyze",


                json=payload


            )
























        response.raise_for_status()









        result = response.json()





        logger.info(

            "Agent Service completed successfully."

        )





        return normalize_agent_response(

            result

        )









    except httpx.HTTPStatusError as exc:



        logger.exception(

            "Agent Service returned an error."

        )



        return {


            "intent":

                "unknown",



            "selected_modules":

                [],



            "execution_order":

                [],



            "reason":

                f"Agent API Error: {exc.response.status_code}"


        }









    except httpx.RequestError:



        logger.exception(

            "Unable to connect to Agent Service."

        )



        return {


            "intent":

                "unknown",



            "selected_modules":

                [],



            "execution_order":

                [],



            "reason":

                "Agent Service unavailable"


        }