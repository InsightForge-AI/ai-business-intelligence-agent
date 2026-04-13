import requests
from config import CV_API_URL
from pathlib import Path


def run_cv(query):

    # query should be image file path

    file_path = Path(query)


    if not file_path.exists():

        return {

            "error": "Image file not found",

            "path": str(file_path)

        }


    with open(file_path, "rb") as f:

        files = {

            "file": (file_path.name, f, "image/jpeg")

        }


        response = requests.post(

            CV_API_URL,

            files=files

        )


    return response.json()