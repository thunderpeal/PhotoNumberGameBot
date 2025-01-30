import base64
import io
import logging
import mimetypes

from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from photonumbergamebot.src.data_managers.texts_handler import game_texts
from photonumbergamebot.src.settings import BOT_TOKEN, EXAMPLE_PHOTO
from photonumbergamebot.src.utils import (
    extract_number_from_photo,
    get_current_number,
    get_restrictions_button,
    statistics_per_user,
    update_current_number,
    update_player_stats,
)

dp = Dispatcher()
router = Router()
dp.include_router(router)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    logger.info(
        f"Received start command from user {message.from_user.username} in chat {message.chat.id}"
    )
    await message.answer(text=game_texts.welcome_text)
    await message.answer_photo(
        photo=EXAMPLE_PHOTO,
        caption=game_texts.photo_example_text,
        reply_markup=get_restrictions_button(),
        show_caption_above_media=True,
    )
    chat_id = str(message.chat.id)
    current_number, who_found_last = await get_current_number(chat_id)
    if not current_number:
        await update_current_number(chat_id, 1, "game")
    logger.info(f"Finished handling start command")


@router.callback_query(F.data == "show_restrictions")
async def show_restrictions(callback: CallbackQuery):
    logger.info(f"Received callback query to show restrictions")
    await callback.message.answer(text=game_texts.restrictions_text)
    await callback.answer("Показываю ограничения!")
    logger.info(f"Finished handling callback query")


@router.message(
    F.photo,
    F.media_group_id.is_(None),
    F.forward_date.is_(None),
    F.forward_from.is_(None),
    F.forward_from_chat.is_(None),
)
async def handle_photo_count(message: types.Message):
    logger.info(f"Received photo message from user {message.from_user.username}")
    chat_id = str(message.chat.id)
    user_name = message.from_user.username
    caption = message.caption
    current_number, who_found_last = await get_current_number(chat_id)

    if caption:
        try:
            number_from_photo = int(caption)
        except ValueError:
            return
    else:
        file = await bot.get_file(message.photo[-1].file_id)
        file_path = file.file_path

        img = await bot.download_file(file_path, io.BytesIO())
        img_bytes = img.read()
        img_b64 = base64.b64encode(img_bytes).decode("utf-8")
        mime_type = mimetypes.guess_type(file_path)[0] or "image/jpeg"

        number_from_photo = await extract_number_from_photo(
            img_b64, mime_type, current_number
        )

    if number_from_photo == current_number:
        if who_found_last == user_name:
            await message.answer(
                f"@{user_name}, ты уже нашел(-a) предыдущее число, теперь очередь других игроков"
            )
            return
        await update_current_number(chat_id, current_number + 1, user_name)
        await update_player_stats(chat_id, user_name)
        await message.answer(
            f"@{user_name} нашел(-a) число {current_number}! Теперь ищем число {current_number + 1}"
        )
    logger.info(f"Finished handling photo message")


@router.message(Command(commands=["statistics"]))
async def show_statistics(message: Message):
    logger.info(f"Received statistics command from user {message.from_user.username}")
    chat_id = str(message.chat.id)
    player_statistics = await statistics_per_user(chat_id)
    if not player_statistics:
        await message.reply("Пока никто ничего не нашел! Продолжайте поиски 🎮")
        return

    medals = ["🥇", "🥈", "🥉"]

    stats = []
    for i, (player, count) in enumerate(player_statistics.items()):
        if i < 3:
            stats.append(f"{medals[i]} {player}: {count}")
        else:
            stats.append(f"{player}: {count}")

    stats_string = "\n".join(stats)

    await message.reply(f"📊 Статистика игроков по найденным числам:\n{stats_string}")


@router.message(Command(commands=["count_from"]))
async def set_starting_number(message: Message):
    args = message.text.split()
    if len(args) != 2 or not args[1].isdigit():
        await message.answer(
            "Пожалуйста, используйте команду правильно: /count_from [число].",
            parse_mode=None,
        )
        return

    new_number = int(args[1])
    chat_id = str(message.chat.id)
    await update_current_number(chat_id, new_number, user_name="game")
    await message.reply(f"Игра продолжится с числа {new_number}. Найдите его!")


@router.message(Command(commands=["rules"]))
async def show_rules(message: Message):
    logger.info(f"Received request for rules from user {message.from_user.username}")
    await message.reply(game_texts.rules_text)
    logger.info(f"Completed request for rules from user {message.from_user.username}")


@router.message(Command(commands=["current_number"]))
async def number_to_find(message: Message):
    logger.info(
        f"Received request for current number from user {message.from_user.username}"
    )
    chat_id = str(message.chat.id)
    current_number, who_found_last = await get_current_number(chat_id)
    if not current_number:
        await message.answer(text="Сначала начните игру через команду /start")
    elif who_found_last == "game":
        await message.answer(text=f"Сейчас ищем число {current_number}")
    else:
        await message.answer(
            text=f"Сейчас ищем число {current_number}. "
            f"Предыдущее фото отправил(-a) @{who_found_last}, теперь очередь других игроков"
        )
    logger.info(
        f"Completed request for current number from user {message.from_user.username}"
    )
