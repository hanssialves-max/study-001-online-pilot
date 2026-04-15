import os
from pathlib import Path


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-before-production")
    BASE_DIR = Path(__file__).resolve().parent.parent
    RAW_DATA_DIR = Path(os.environ.get("RAW_DATA_DIR", BASE_DIR / "data" / "raw"))
    EXPORT_DATA_DIR = Path(os.environ.get("EXPORT_DATA_DIR", BASE_DIR / "data" / "exports"))
    COMPLETION_CODE = os.environ.get("COMPLETION_CODE", "REPLACE_WITH_REAL_CODE")
    PROLIFIC_RETURN_URL = os.environ.get("PROLIFIC_RETURN_URL", "")
    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"
