"""
==========================================================
Backend Settings
==========================================================

Application configuration.

Responsibilities
----------------
• Storage paths
• Supported file types
• Upload limits
"""

from pathlib import Path


# ---------------------------------------------------------
# Project Directories
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

STORAGE_DIR = BASE_DIR / "storage"

UPLOAD_DIRECTORY = STORAGE_DIR / "uploads"

TEMP_UPLOAD_DIRECTORY = STORAGE_DIR / "temp_uploads"

METADATA_DIRECTORY = STORAGE_DIR / "metadata"


# ---------------------------------------------------------
# Upload Settings
# ---------------------------------------------------------

MAX_UPLOAD_SIZE = 100 * 1024 * 1024      # 100 MB


# ---------------------------------------------------------
# Supported File Types
# ---------------------------------------------------------

SUPPORTED_EXTENSIONS = {

    ".pdf",

    ".docx",

    ".csv",

    ".xlsx",

    ".xls",

    ".png",

    ".jpg",

    ".jpeg"

}


SUPPORTED_MIME_TYPES = {

    "application/pdf",

    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",

    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

    "application/vnd.ms-excel",

    "text/csv",

    "image/png",

    "image/jpeg"

}


# ---------------------------------------------------------
# Create Storage Directories
# ---------------------------------------------------------

UPLOAD_DIRECTORY.mkdir(

    parents=True,

    exist_ok=True

)

TEMP_UPLOAD_DIRECTORY.mkdir(

    parents=True,

    exist_ok=True

)

METADATA_DIRECTORY.mkdir(

    parents=True,

    exist_ok=True

)