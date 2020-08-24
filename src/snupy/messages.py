import os
import re
import random

COMPLIMENT_PATTERN = re.compile(r"(褒|ほ)めて|(頑張|がんば|がむば|がむぱ)った")
NEGATIVE_PATTERN = re.compile(r"(辛|つら)い|(頑張|がんば|がむば|がむぱ)る")
CHOICE_PATTERN = re.compile(r"choice (?P<items>.*)")


def get_response_text(message):
    if message == "maxim":
        return _choose_maxim()

    elif COMPLIMENT_PATTERN.search(message):
        return "えらい！！！"

    elif NEGATIVE_PATTERN.search(message):
        return "ぱにゃにゃんだー🐼😺"

    elif message.startswith("choice"):
        m = CHOICE_PATTERN.match(message)
        return _choose_one(re.split(",|、", m.group("items")))

    return message


def _choose_maxim():
    maxim_file_path = os.path.join(os.path.dirname(__file__), "resources", "maxim.txt")
    with open(maxim_file_path) as maxim_file:
        maxims = maxim_file.readlines()
        return random.choice(maxims)


def _choose_one(options):
    chosen = random.choice(options)
    return f"I choose this 👉 {chosen.strip()}"
