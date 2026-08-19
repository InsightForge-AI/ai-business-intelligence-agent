"""
==========================================================
NLP Service
==========================================================

Backend client for the Natural Language Processing Service.

Responsibilities
----------------
• Send extracted text to NLP module
• Receive summary and insights
• Normalize NLP response
"""

import httpx


from config.endpoints import NLP_API

from utils.logger import logger





def normalize_nlp_response(response: dict):


    return {


        "module":"nlp",


        "success":

            response.get(

                "success",

                True

            ),



        "summary":

            response.get(

                "summary",

                {

                    "overview":"",

                    "metrics":[],

                    "highlights":[],

                    "executiveSummary":"",

                    "recommendations":[]

                }

            ),



        "insights":

            response.get(

                "insights",

                {

                    "confidence":0,

                    "entities":[],

                    "keywords":[],

                    "key_findings":[],

                    "risks":[],

                    "opportunities":[],

                    "suggestions":[]

                }

            )

    }









async def run_nlp(

    query: str,

    content,

    metadata: dict

) -> dict:


    # -----------------------------------------------------
    # Normalize extracted content
    # -----------------------------------------------------

    if isinstance(content, dict):


        if "text" in content:


            content = content["text"]


        elif "content" in content:


            content = content["content"]


        else:


            content = str(content)


    else:


        content = str(content)









    payload = {


        "query":query,


        "content":content,


        "metadata":metadata


    }





    logger.info(

        "Calling NLP Service..."

    )




















    try:


        async with httpx.AsyncClient(

            timeout=300

        ) as client:



            response = await client.post(


                f"{NLP_API}/nlp/analyze",


                json=payload


            )
























        response.raise_for_status()









        result = response.json()





        logger.info(

            "NLP Service completed successfully."

        )





        return normalize_nlp_response(

            result

        )









    except httpx.HTTPStatusError as exc:



        logger.exception(

            "NLP Service returned an error."

        )



        return {


            "module":"nlp",


            "success":False,


            "message":

                f"NLP API Error: {exc.response.status_code}"


        }









    except httpx.RequestError:



        logger.exception(

            "Unable to connect to NLP Service."

        )



        return {


            "module":"nlp",


            "success":False,


            "message":

                "NLP Service is unavailable."


        }