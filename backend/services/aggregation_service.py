"""
==========================================================
Aggregation Service
==========================================================

Responsibilities
----------------
• Merge AI module responses
• Extract Summary
• Extract Insights
• Handle partial failures
• Return standardized response
"""

from datetime import datetime





def default_summary():

    return {


        "overview":"",


        "metrics":[],


        "highlights":[],


        "executiveSummary":"",


        "recommendations":[]


    }









def default_insights():

    return {


        "confidence":0,


        "entities":[],


        "keywords":[],


        "key_findings":[],


        "risks":[],


        "opportunities":[],


        "suggestions":[]


    }









def aggregate_results(

    file_info: dict,

    routing: dict,

    results: list

) -> dict:



    aggregated = {


        "success":True,



        "file":{


            "id":

            file_info.get(

                "file_id"

            ),



            "name":

            file_info.get(

                "file_name"

            ),



            "type":

            file_info.get(

                "file_type"

            )


        },





        "agent":{


            "intent":

            routing.get(

                "intent",

                ""

            ),



            "modules":

            routing.get(

                "selected_modules",

                []

            ),



            "execution_order":

            routing.get(

                "execution_order",

                []

            ),



            "reason":

            routing.get(

                "reason",

                ""

            )


        },





        "results":{},



        "summary":

        default_summary(),



        "insights":

        default_insights(),



        "errors":[],



        "generated_at":

        datetime.utcnow().isoformat()


    }









    for result in results:



        if result is None:

            continue









        # -----------------------------------------
        # Exception Handling
        # -----------------------------------------

        if isinstance(

            result,

            Exception

        ):


            aggregated["errors"].append({


                "module":"unknown",


                "message":str(result)


            })


            continue









        module = result.get(

            "module",

            "unknown"

        )









        if result.get(

            "success",

            False

        ):



            aggregated["results"][

                module

            ] = result







            # -------------------------------------
            # Extract Summary
            # -------------------------------------

            if result.get(

                "summary"

            ):


                aggregated["summary"].update(

                    result["summary"]

                )









            # -------------------------------------
            # Extract Insights
            # -------------------------------------

            if result.get(

                "insights"

            ):


                aggregated["insights"].update(

                    result["insights"]

                )









        else:



            aggregated["errors"].append({


                "module":module,


                "message":

                    result.get(

                        "message",

                        "Unknown error"

                    )


            })









    # -------------------------------------------------
    # Final Status
    # -------------------------------------------------

    if aggregated["errors"]:


        aggregated["success"] = False









    return aggregated