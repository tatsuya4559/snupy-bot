import os
import re
import random

from bottle import run, post, request, abort, default_app
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
)

app = default_app()

line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN", ""))
handler = WebhookHandler(os.getenv("CHANNEL_SECRET", ""))


@post("/api/line/callback")
def callback():
    signature = request.get_header("X-Line-Signature")
    body = request.body.getvalue().decode()

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


COMPLIMENT_PATTERN = re.compile(r"(褒|ほ)めて|(頑張|がんば|がむば|がむぱ)った")
NEGATIVE_PATTERN = re.compile(r"(辛|つら)い|(頑張|がんば|がむば|がむぱ)る")


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    response_text = text

    if text == "maxim":
        response_text = _choose_maxim()

    elif COMPLIMENT_PATTERN.search(text):
        response_text = "えらい！！！"

    elif NEGATIVE_PATTERN.search(text):
        response_text = "ぱにゃにゃんだー🐼😺"

    elif text.startswith("choice"):
        regex = re.compile(r"choice (?P<items>.*)")
        m = regex.match(text)
        response_text = _choose_one(re.split(",|、", m.group("items")))

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response_text))


def _choose_maxim():
    maxim_file_path = os.path.join(os.getcwd(), "resources", "maxim.txt")
    with open(maxim_file_path) as maxim_file:
        maxims = maxim_file.readlines()
        return random.choice(maxims)


def _choose_one(options):
    chosen = random.choice(options)
    return f"I choose this 👉 {chosen.strip()}"


if __name__ == "__main__":
    run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
