# Photo Number Game Bot
__by @thunderpeal__
You can try this bot at https://t.me/photo_number_game_bot

Telegram bot based on aiogram for a fun game. With PostgreSQL as a database.

Enviromental variables:

```.dotenv
PYTHONUNBUFFERED=1
DATABASE_URL=<your postgresql url>
BOT_TOKEN=<your telegram bot token>
EXAMPLE_PHOTO=<photo url from google>
RESOURCES_PATH=./photonumbergamebot/resources
# TESSERACT_PATH=# currently in development
```

How to use:

1. Add the bot to your Telegram group.
2. Start the game by sending the `/start` command.


*Game Rules*

1. *The goal of the game* is to find numbers in the real world in ascending order, starting with 1, and send their photos to the chat.

2. *How to play:*
- See a number that corresponds to the current step of the game? Take a photo of it and send it to the chat.
- Numbers can be on any objects: house numbers, page numbers, tickets, price tags, etc.

3. *Restrictions:*
- Numbers must be whole (for example, you cannot use 14.01 as 14, 1098 as 98).
- You cannot use text written or drawn by yourself.
- One source cannot be used more than once a day (for example, the same sign or presentation).
- The same participant cannot send two numbers in a row - participants must alternate.

4. *Commands:*
- `/current_number` - what number we are currently looking for.
- `/count_from [number]` – continue the game from the specified number.
- `/statistics` – show which of the chat participants guessed how many numbers.
- `/rules` – show the rules of the game.

The game continues until the participants find the numbers!