import logging
import os

from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

BOT_TOKEN: str = os.environ.get("BOT_TOKEN", "")
EXAMPLE_PHOTO: str = os.environ.get("EXAMPLE_PHOTO", "")
RESOURCES_PATH: str = os.environ.get("RESOURCES_PATH", "")
TESSERACT_PATH: str = os.environ.get("TESSERACT_PATH", "")
DATABASE_URL: str = os.environ.get("DATABASE_URL", "")

logger.info("Successfully extracted app settings")

__all__ = [
    "BOT_TOKEN",
    "EXAMPLE_PHOTO",
    "RESOURCES_PATH",
    "TESSERACT_PATH",
    "DATABASE_URL",
]
