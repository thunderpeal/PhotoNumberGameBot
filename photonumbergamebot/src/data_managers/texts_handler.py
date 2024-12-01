import os.path
from dataclasses import dataclass

from photonumbergamebot.src.settings import RESOURCES_PATH


@dataclass
class PhotoNumberGameBotTexts:
    welcome_text: str = ""
    photo_example_text: str = ""
    restrictions_text: str = ""
    rules_text: str = ""

    def __post_init__(self):
        with open(
            os.path.join(RESOURCES_PATH, "texts", "hello.txt"), "r", encoding="utf-8"
        ) as welcome_text:
            self.welcome_text = welcome_text.read()
        with open(
            os.path.join(RESOURCES_PATH, "texts", "example.txt"), "r", encoding="utf-8"
        ) as photo_example:
            self.photo_example_text = photo_example.read()
        with open(
            os.path.join(RESOURCES_PATH, "texts", "restrictions.txt"), "r", encoding="utf-8"
        ) as restrictions:
            self.restrictions_text = restrictions.read()
        with open(
            os.path.join(RESOURCES_PATH, "texts", "rules.txt"), "r", encoding="utf-8"
        ) as rules:
            self.rules_text = rules.read()


game_texts = PhotoNumberGameBotTexts()
