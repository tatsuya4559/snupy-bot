import os
import re
import random
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN", ""))
handler = WebhookHandler(os.getenv("CHANNEL_SECRET", ""))


@app.route("/api/line/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

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
    maxim_file_path = os.path.join(app.root_path, "resources", "maxim.txt")
    with open(maxim_file_path) as maxim_file:
        maxims = maxim_file.readlines()
        return random.choice(maxims)


def _choose_one(options):
    chosen = random.choice(options)
    return f"I choose this 👉 {chosen.strip()}"


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage="Usage: python " + __file__ + " [--port <port>] [--help]"
    )
    arg_parser.add_argument("-p", "--port", default=8000, help="port")
    arg_parser.add_argument("-d", "--debug", default=False, help="debug")
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
