import logging
import os

from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

BOT_TOKEN: str = os.environ.get("BOT_TOKEN", "")
EXAMPLE_PHOTO: str = os.environ.get("EXAMPLE_PHOTO", "")
RESOURCES_PATH: str = os.environ.get("RESOURCES_PATH", "")
DATABASE_URL: str = os.environ.get("DATABASE_URL", "")
MODEL_API_URL: str = os.environ.get("MODEL_API_URL", "")
MODEL_API_TOKEN: str = os.environ.get("MODEL_API_TOKEN", "")
MODEL: str = os.environ.get("MODEL", "Qwen/Qwen2-VL-7B-Instruct")
SUPPORT_LINK: str = os.environ.get("SUPPORT_LINK", "")

logger.info("Successfully extracted app settings")

__all__ = [
    "BOT_TOKEN",
    "EXAMPLE_PHOTO",
    "RESOURCES_PATH",
    "DATABASE_URL",
    "MODEL_API_URL",
    "MODEL_API_TOKEN",
    "MODEL",
    "SUPPORT_LINK",
]
