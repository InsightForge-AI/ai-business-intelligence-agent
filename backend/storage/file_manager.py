"""
==========================================================
File Manager
==========================================================

Responsibilities
----------------
• Save uploaded files
• Delete files

No business logic.
"""

from pathlib import Path
import shutil

from fastapi import UploadFile

from config.settings import UPLOAD_DIRECTORY


def save_file(
    file: UploadFile,
    filename: str
) -> str:
    """
    Save uploaded file.

    Parameters
    ----------
    file : UploadFile

    filename : str

    Returns
    -------
    str
    """

    upload_dir = Path(

        UPLOAD_DIRECTORY

    )

    upload_dir.mkdir(

        parents=True,

        exist_ok=True

    )

    file_path = upload_dir / filename

    with open(

        file_path,

        "wb"

    ) as buffer:

        shutil.copyfileobj(

            file.file,

            buffer

        )

    return str(

        file_path

    )


def delete_file(
    file_path: str
):
    """
    Delete a stored file.
    """

    Path(

        file_path

    ).unlink(

        missing_ok=True

    )