"""
==========================================================
Cleanup Utility
==========================================================

Responsibilities
----------------
• Remove expired uploaded files
• Remove expired metadata
"""

import time
from pathlib import Path

from config.settings import (
    UPLOAD_DIRECTORY,
    METADATA_DIRECTORY
)

from utils.logger import logger


FILE_EXPIRY_SECONDS = 1800


def cleanup_files():
    """
    Delete expired uploaded files and metadata.
    """

    current_time = time.time()

    upload_dir = Path(UPLOAD_DIRECTORY)

    metadata_dir = Path(METADATA_DIRECTORY)

    for file_path in upload_dir.iterdir():

        if not file_path.is_file():

            continue

        file_age = current_time - file_path.stat().st_mtime

        if file_age <= FILE_EXPIRY_SECONDS:

            continue

        file_id = file_path.stem

        metadata_file = metadata_dir / f"{file_id}.json"

        try:

            file_path.unlink(
                missing_ok=True
            )

            metadata_file.unlink(
                missing_ok=True
            )

            logger.info(

                f"Deleted expired file: {file_path.name}"

            )

        except Exception as exc:

            logger.exception(

                f"Failed to delete {file_path.name}: {exc}"

            )