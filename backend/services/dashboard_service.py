"""
==========================================================
Dashboard Service
==========================================================

Responsibilities
----------------
• Build dashboard response
• Read uploaded document metadata
• Generate workspace statistics
• Return frontend dashboard data

No AI processing.
"""

import json


from config.settings import (
    METADATA_DIRECTORY,
    UPLOAD_DIRECTORY
)







# ---------------------------------------------------------
# Dashboard
# ---------------------------------------------------------

async def get_dashboard() -> dict:
    """
    Build complete dashboard response.
    """



    metadata_files = sorted(

        METADATA_DIRECTORY.glob("*.json"),

        key=lambda file:file.stat().st_mtime,

        reverse=True

    )





    documents = []


    total_storage = 0





    for file in metadata_files:


        try:


            data = json.loads(

                file.read_text(

                    encoding="utf-8"

                )

            )



            documents.append(data)



            total_storage += data.get(

                "file_size",

                0

            )



        except Exception:


            continue







    total_documents = len(documents)



    latest = (

        documents[0]

        if documents

        else {}

    )








    # -----------------------------------------------------
    # File Types
    # -----------------------------------------------------

    file_types = {}



    for document in documents:


        file_type = document.get(

            "file_type",

            "unknown"

        )



        file_types[file_type] = (

            file_types.get(

                file_type,

                0

            ) + 1

        )









    storage_mb = round(

        total_storage /

        (1024 * 1024),

        2

    )









    # -----------------------------------------------------
    # Intelligence Graph
    # -----------------------------------------------------

    intelligence_graph = {


        "nodes":[


            {


                "id":key,


                "label":key.upper(),


                "value":value


            }


            for key,value in file_types.items()

        ],





        "statistics":{


            "documents":

                total_documents,



            "fileTypes":

                len(file_types),



            "storageMB":

                storage_mb

        }


    }









    # -----------------------------------------------------
    # Workspace Health
    # -----------------------------------------------------

    workspace_health = {


        "status":

            "Healthy",



        "summary":

            f"{total_documents} documents available in workspace",



        "items":[


            {


                "id":"documents",


                "label":"Documents",


                "value":

                    f"{total_documents} Files",


                "icon":"file"


            },



            {


                "id":"storage",


                "label":"Storage",


                "value":

                    f"{storage_mb} MB",


                "icon":"storage"


            },



            {


                "id":"ai",


                "label":"AI Core",


                "value":

                    "Ready",


                "icon":"brain"


            },



            {


                "id":"vector",


                "label":"Vector DB",


                "value":

                    "Ready"

                    if total_documents > 0

                    else "Empty",


                "icon":"database"


            },



            {


                "id":"queue",


                "label":"Queue",


                "value":

                    "0 Jobs",


                "icon":"activity"


            },



            {


                "id":"workspace",


                "label":"Workspace",


                "value":

                    "Healthy",


                "icon":"workspace"


            }


        ],





        "statistics":{


            "totalDocuments":

                total_documents,



            "storageUsed":

                storage_mb,



            "uploadDirectory":

                str(

                    UPLOAD_DIRECTORY

                )

        }


    }









    # -----------------------------------------------------
    # Active Document
    # -----------------------------------------------------

    active_document = None





    if latest:


        active_document = {


            "id":

                latest.get(

                    "file_id"

                ),



            "name":

                latest.get(

                    "file_name",

                    ""

                ),



            "type":

                latest.get(

                    "file_type",

                    ""

                ),



            "size":

                latest.get(

                    "file_size",

                    0

                ),



            "status":

                latest.get(

                    "status",

                    "Uploaded"

                ),



            "aiReady":

                bool(

                    latest.get(

                        "summary"

                    )

                ),



            "hasSummary":

                bool(

                    latest.get(

                        "summary"

                    )

                ),



            "hasInsights":

                bool(

                    latest.get(

                        "insights"

                    )

                ),



            "summary":

                latest.get(

                    "summary"

                ),



            "insights":

                latest.get(

                    "insights"

                )

        }









    # -----------------------------------------------------
    # Upload Configuration
    # -----------------------------------------------------

    upload_analyze = {


        "supportedFormats":[


            ".pdf",

            ".doc",

            ".docx",

            ".txt",

            ".csv",

            ".xlsx",

            ".png",

            ".jpg",

            ".jpeg"


        ],



        "maximumFiles":1,



        "analysisEnabled":True

    }









    # -----------------------------------------------------
    # AI Workflow Information
    # -----------------------------------------------------

    ai_workflows = {


        "modules":[


            "Agent",

            "ML",

            "NLP",

            "RAG",

            "CV"


        ],



        "totalModules":5,



        "parallelExecution":True

    }









    return {


        "intelligenceGraph":

            intelligence_graph,



        "workspaceHealth":

            workspace_health,



        "activeDocument":

            active_document,



        "uploadAnalyze":

            upload_analyze,



        "aiWorkflows":

            ai_workflows

    }