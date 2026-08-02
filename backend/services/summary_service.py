from utils.logger import logger

from services.nlp_service import run_nlp





async def generate_document_summary(document):


    try:


        text = document.get(

            "extracted_text",

            ""

        )



        if not text:


            raise ValueError(

                "Extracted text not found"

            )







        metadata = {


            "document_id":

            document.get("file_id"),



            "document_name":

            document.get("file_name"),



            "document_type":

            document.get("file_type")

        }







        result = await run_nlp(


            query="""

            Analyze this document.

            Return JSON format:

            {

                "summary":"",

                "keywords":[],

                "entities":[],

                "recommendations":[],

                "topics":[],

                "sentiment":""

            }


            """,


            content=text,


            metadata=metadata

        )









        print("\n========== NLP RESPONSE ==========")

        print(result)

        print("==================================\n")




        logger.info(

            f"NLP Response: {result}"

        )







        if "data" in result:

            result = result["data"]







        # =====================================
        # DOCUMENT SUMMARY
        # =====================================

        summary = {


            "overview":

            result.get(

                "summary",

                ""

            ),



            "metrics":

            [],



            "highlights":

            result.get(

                "keywords",

                []

            ),



            "executiveSummary":

            result.get(

                "summary",

                ""

            ),



            "recommendations":

            result.get(

                "recommendations",

                []

            )

        }









        # =====================================
        # DOCUMENT INSIGHTS
        # =====================================

        insights = {


            "confidence":

            90,



            "entities":

            result.get(

                "entities",

                []

            ),



            "keywords":

            result.get(

                "keywords",

                []

            ),



            "key_findings":

            [

                result.get(

                    "summary",

                    ""

                )

            ],



            "risks":

            [],



            "opportunities":

            [],



            "suggestions":

            result.get(

                "recommendations",

                []

            )


        }









        return {


            "summary":

            summary,



            "insights":

            insights


        }









    except Exception as error:


        logger.exception(

            f"Summary generation failed: {error}"

        )


        raise error