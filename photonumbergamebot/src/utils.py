import logging
import sys

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from openai import OpenAI

from photonumbergamebot.src.data_managers.db_controller import db_manager
from photonumbergamebot.src.settings import MODEL, MODEL_API_TOKEN, MODEL_API_URL

SYSTEM_PROMPT = """
You will receive an image containing one or more numbers and a text input with a single number. Your task is to analyze the image and determine if the exact number from the text input appears as a whole number in the image.

Rules:
Respond with 'y' if the number from the text input exactly matches a number in the image.
Respond with 'n' if the number from the text input is part of a larger number in the image (for example, '11' should not match '1132').
Respond with 'n' if the number from the text input does not appear in the image at all.

---------------------

Examples:
Example 1:
Text input: "1132"
Image: 1132
Response: 'y'
Explanation: The number "1132" exactly matches the number in the image.

Example 2:
Text input: "11"
Image: 1132
Response: 'n'
Explanation: "11" is part of the number "1132," but not a separate number.

Example 3:
Text input: "45"
Image: 345 450 12
Response: 'n'
Explanation: "45" is part of the numbers "450" and "345," but not a separate number.

Example 4:
Text input: "123"
Image: 123, 456, 789
Response: 'y'
Explanation: "123" exactly matches a number in the image.

Example 5:
Text input: "78"
Image: 123, 789, 567
Response: 'n'
Explanation: "78" does not appear as a standalone number in the image.

Example 6:
Text input: "9"
Image: 9 9 9
Response: 'y'
Explanation: "9" appears as a standalone number in the image.

Output:
Respond only with 'y' or 'n' with no additional explanations.
"""

llm_client = OpenAI(
    base_url=MODEL_API_URL,
    api_key=MODEL_API_TOKEN,
)


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


async def get_current_number(chat_id: str) -> tuple[int | None, str | None]:
    game_state = db_manager.get_game_state(chat_id)
    if game_state:
        return game_state.number_to_find, game_state.who_found_last
    else:
        return None, None


async def update_current_number(chat_id: str, new_number: int, user_name: str) -> None:
    db_manager.update_game_state(chat_id, new_number, user_name)


async def extract_number_from_photo(img_b64_str, img_type, current_number: int):
    response = llm_client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": str(current_number)},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"""data:{img_type};base64,{img_b64_str}"""
                        },
                    },
                ],
            },
        ],
    )

    answer = response.choices[0].message.content
    if "y" in answer.lower():
        return current_number
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
