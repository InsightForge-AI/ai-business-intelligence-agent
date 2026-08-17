"""
==========================================================
Storage Service
==========================================================

Responsibilities
----------------
• Validate uploaded files
• Generate unique file IDs
• Save uploaded files
• Store metadata
• Retrieve uploaded files
• Delete uploaded files

No AI processing.
"""

import json

from pathlib import Path

from uuid import uuid4

from fastapi import UploadFile


from config.settings import (
    UPLOAD_DIRECTORY,
    METADATA_DIRECTORY,
    SUPPORTED_EXTENSIONS,
    MAX_UPLOAD_SIZE
)


from utils.logger import logger



# ---------------------------------------------------------
# Ensure Storage Directories Exist
# ---------------------------------------------------------

UPLOAD_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)


METADATA_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)


# ---------------------------------------------------------
# Save Uploaded File
# ---------------------------------------------------------

async def save_uploaded_file(
    file: UploadFile
) -> dict:
    """
    Save uploaded document.
    """

    extension = Path(

        file.filename

    ).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:

        raise ValueError(

            f"Unsupported file type: {extension}"

        )

    file_id = str(

        uuid4()

    )

    stored_filename = f"{file_id}{extension}"

    destination = (

        UPLOAD_DIRECTORY /

        stored_filename

    )

    contents = await file.read()

    if len(contents) > MAX_UPLOAD_SIZE:

        raise ValueError(

            f"File exceeds maximum upload size of {MAX_UPLOAD_SIZE} bytes"

        )

    destination.write_bytes(

        contents

    )

    file_info = {

    "id": file_id,

    "file_id": file_id,

    "name": file.filename,

    "file_name": file.filename,

    "file_path": str(destination),

    "file_type": extension,

    "file_size": len(contents),

    "status": "Uploaded"

}

    metadata_file = (

        METADATA_DIRECTORY /

        f"{file_id}.json"

    )

    metadata_file.write_text(

    json.dumps(

        file_info,

        indent=4,

        ensure_ascii=False

    ),

    encoding="utf-8"

)

    logger.info(

        f"Stored file: {file.filename}"

    )

    return file_info


# ---------------------------------------------------------
# Retrieve Uploaded File
# ---------------------------------------------------------

def get_uploaded_file(
    file_id: str
) -> dict:
    """
    Retrieve uploaded file information.
    """

    metadata_file = (

        METADATA_DIRECTORY /

        f"{file_id}.json"

    )

    if not metadata_file.exists():

        raise FileNotFoundError(

            f"File not found: {file_id}"

        )

    return json.loads(

        metadata_file.read_text()

    )


# ---------------------------------------------------------
# Delete Uploaded File
# ---------------------------------------------------------

def delete_uploaded_file(
    file_id: str
):
    """
    Delete uploaded file and metadata.
    """

    file_info = get_uploaded_file(

        file_id

    )

    Path(

        file_info["file_path"]

    ).unlink(

        missing_ok=True

    )

    (

        METADATA_DIRECTORY /

        f"{file_id}.json"

    ).unlink(

        missing_ok=True

    )

    logger.info(

        f"Deleted file: {file_id}"

    )