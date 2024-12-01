import asyncio

from photonumbergamebot.src.bot import bot, dp
from photonumbergamebot.src.utils import setup_logging


async def main() -> None:
    """
    Start the bot in polling mode.
    This function runs the bot in an infinite loop until the program is
    stopped. It should be called once at the end of the program.
    """
    await dp.start_polling(bot)


if __name__ == "__main__":
    logger = setup_logging()
    asyncio.run(main())
    logger.info('Приложение запущено')
