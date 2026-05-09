import requests
from config import CV_API_URL


def run_cv(image_path):

    try:

        with open(image_path, "rb") as f:

            files = {
                "file": (
                    image_path,
                    f,
                    "image/jpeg"
                )
            }

            response = requests.post(
                CV_API_URL,
                files=files,
                timeout=120
            )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        return {
            "error": str(e)
        }