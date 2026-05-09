import requests
from config import CV_API_URL
from pathlib import Path


def run_cv(query):

    try:

        file_path = Path(query)

        if not file_path.exists():

            return {

                "error": "Image file not found",

                "path": str(file_path)

            }

        with open(file_path, "rb") as f:

            files = {

                "file": (
                    file_path.name,
                    f,
                    "image/jpeg"
                )

            }

            response = requests.post(
                CV_API_URL,
                files=files,
                timeout=60
            )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        return {
            "error": str(e)
        }