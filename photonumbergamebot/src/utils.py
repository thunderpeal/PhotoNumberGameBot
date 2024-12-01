# import pytesseract
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from photonumbergamebot.src.data_managers.db_controller import db_manager
from photonumbergamebot.src.settings import TESSERACT_PATH

# pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
import logging
import sys


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler("app.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


async def get_current_number(chat_id: str) -> tuple[int, str]:
    game_state = db_manager.get_game_state(chat_id)
    if game_state:
        return game_state.number_to_find, game_state.who_found_last
    else:
        return 1, "game"


async def update_current_number(chat_id: str, new_number: int, user_name: str) -> None:
    db_manager.update_game_state(chat_id, new_number, user_name)


async def extract_number_from_photo(message):
    # Realization of OCR is to be done
    return -1


async def update_player_stats(chat_id: str, player_name: str) -> None:
    db_manager.update_player_stat(chat_id, player_name)


def get_restrictions_button() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔎 Подробнее об ограничениях",
                    callback_data="show_restrictions",
                )
            ]
        ]
    )
    return keyboard


async def statistics_per_user(chat_id: str) -> dict[str:int] | None:
    sorted_users = db_manager.get_player_stats(chat_id)
    if not sorted_users:
        return None
    user_stats = {f"@{user.player_name}": user.found_numbers for user in sorted_users}
    return user_stats
