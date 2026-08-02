"""
==========================================================
Orchestration Service
==========================================================

Central workflow coordinator for DocuMind.

Workflow
--------
Storage
    ↓
Extraction
    ↓
Metadata
    ↓
Agent
    ↓
ML / NLP / RAG / CV
    ↓
Aggregation
    ↓
Summary + Insights
"""

import asyncio


from services.storage_service import get_uploaded_file

from services.extraction_service import extract_document

from services.metadata_service import generate_metadata


from services.agent_service import run_agent


from services.ml_service import run_ml

from services.nlp_service import run_nlp

from services.rag_service import run_rag

from services.cv_service import run_cv


from services.aggregation_service import aggregate_results


from utils.logger import logger







# ---------------------------------------------------------
# Available AI Modules
# ---------------------------------------------------------

MODULE_SERVICES = {


    "ml": run_ml,


    "nlp": run_nlp,


    "rag": run_rag,


    "cv": run_cv


}









# ---------------------------------------------------------
# Default Insights Structure
# ---------------------------------------------------------

def create_default_insights():

    return {


        "confidence":0,


        "entities":[],


        "keywords":[],


        "key_findings":[],


        "risks":[],


        "opportunities":[],


        "suggestions":[]


    }









# ---------------------------------------------------------
# Default Summary Structure
# ---------------------------------------------------------

def create_default_summary():

    return {


        "overview":"",


        "metrics":[],


        "highlights":[],


        "executiveSummary":"",


        "recommendations":[]


    }









# ---------------------------------------------------------
# Main Workflow
# ---------------------------------------------------------

async def run_analysis(

    file_id:str,

    query:str

)->dict:


    logger.info(

        f"Starting analysis for file: {file_id}"

    )





    # --------------------------------------------------
    # Load File
    # --------------------------------------------------

    file_info = get_uploaded_file(

        file_id

    )





    logger.info(

        "File loaded successfully"

    )









    # --------------------------------------------------
    # Extraction
    # --------------------------------------------------

    extracted_data = extract_document(

        file_info["file_path"]

    )





    logger.info(

        "Extraction completed"

    )









    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    metadata = generate_metadata(

        file_info=file_info,

        extracted_data=extracted_data

    )









    # --------------------------------------------------
    # Agent Routing
    # --------------------------------------------------

    routing = await run_agent(

        query=query,

        metadata=metadata

    )





    selected_modules = routing.get(

        "selected_modules",

        []

    )





    if not selected_modules:


        logger.warning(

            "No modules selected"

        )


        return {


            "success":False,


            "message":

            "No AI modules selected",


            "summary":

            create_default_summary(),


            "insights":

            create_default_insights()


        }









    logger.info(

        f"Selected modules: {selected_modules}"

    )









    extracted_content = extracted_data.get(

        "content",

        ""

    )









    # --------------------------------------------------
    # Execute AI Modules
    # --------------------------------------------------

    tasks=[]





    for module in selected_modules:


        module = module.lower()



        service = MODULE_SERVICES.get(

            module

        )



        if not service:


            logger.warning(

                f"Unknown module {module}"

            )


            continue





        if module == "cv":


            tasks.append(

                service(

                    query=query,

                    content=file_info["file_path"],

                    metadata=metadata

                )

            )



        else:


            tasks.append(

                service(

                    query=query,

                    content=extracted_content,

                    metadata=metadata

                )

            )









    results = await asyncio.gather(

        *tasks,

        return_exceptions=True

    )









    # --------------------------------------------------
    # Aggregate Response
    # --------------------------------------------------

    final_response = aggregate_results(

        file_info=file_info,

        routing=routing,

        results=results

    )









    # --------------------------------------------------
    # Normalize AI Response
    # --------------------------------------------------

    final_response["summary"] = (

        final_response.get(

            "summary"

        )

        or

        create_default_summary()

    )





    final_response["insights"] = (

        final_response.get(

            "insights"

        )

        or

        create_default_insights()

    )









    # Attach metadata

    final_response["file"] = {


        "id":file_id,


        "name":

            file_info.get(

                "file_name"

            ),


        "type":

            file_info.get(

                "file_type"

            )


    }









    logger.info(

        "Analysis workflow completed successfully"

    )





    return final_response