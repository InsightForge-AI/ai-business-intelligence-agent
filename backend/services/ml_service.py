"""
==========================================================
ML Service
==========================================================

Backend client for Machine Learning Service.

Responsibilities
----------------
• Send CSV/XLSX analysis request
• Receive ML response
• Normalize KPI and insights output
"""

import httpx


from config.endpoints import ML_API

from utils.logger import logger







def normalize_ml_response(response: dict):


    return {


        "module":"ml",



        "success":

            response.get(

                "success",

                True

            ),





        "summary":

            {


                "overview":

                    response.get(

                        "summary",

                        response.get(

                            "analysis",

                            ""

                        )

                    ),



                "metrics":

                    response.get(

                        "kpis",

                        []

                    ),



                "highlights":

                    response.get(

                        "highlights",

                        []

                    ),



                "executiveSummary":

                    response.get(

                        "summary",

                        ""

                    ),



                "recommendations":

                    response.get(

                        "recommendations",

                        []

                    )


            },







        "insights":

            {


                "confidence":

                    response.get(

                        "confidence",

                        90

                    ),



                "entities":

                    response.get(

                        "entities",

                        []

                    ),



                "keywords":

                    response.get(

                        "keywords",

                        []

                    ),



                "key_findings":

                    response.get(

                        "findings",

                        []

                    ),



                "risks":

                    response.get(

                        "risks",

                        []

                    ),



                "opportunities":

                    response.get(

                        "opportunities",

                        []

                    ),



                "suggestions":

                    response.get(

                        "recommendations",

                        []

                    )


            }

    }









async def run_ml(

    query:str,

    content,

    metadata:dict

)->dict:



    payload = {


        "query":

            query,



        "content":

            content,



        "metadata":

            metadata


    }





    logger.info(

        "Calling ML Service..."

    )





    print(

        "\n========== ML PAYLOAD =========="

    )


    print(

        metadata

    )


    print(

        "================================\n"

    )









    try:



        async with httpx.AsyncClient(

            timeout=300

        ) as client:



            response = await client.post(


                f"{ML_API}/ml/analyze",


                json=payload


            )









        print(

            "\n========== ML RESPONSE =========="

        )


        print(

            response.status_code

        )


        print(

            response.text

        )


        print(

            "=================================\n"

        )









        response.raise_for_status()









        result = response.json()





        logger.info(

            "ML Service completed successfully."

        )





        return normalize_ml_response(

            result

        )









    except httpx.HTTPStatusError as exc:



        logger.exception(

            "ML Service returned an error."

        )



        return {


            "module":"ml",


            "success":False,


            "message":

                f"ML API Error: {exc.response.status_code}"


        }









    except httpx.RequestError:



        logger.exception(

            "Unable to connect to ML Service."

        )



        return {


            "module":"ml",


            "success":False,


            "message":

                "ML Service is unavailable."


        }