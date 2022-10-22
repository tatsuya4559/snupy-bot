import os

from chalice import Chalice, BadRequestError
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
)

from chalicelib.messages import get_response_text

app = Chalice(app_name="snupy-bot")

line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN", ""))
handler = WebhookHandler(os.getenv("CHANNEL_SECRET", ""))


@app.route("/api/line/callback", methods=["POST"])
def callback():
    request = app.current_request
    signature = request.headers["X-Line-Signature"]
    body = request.raw_body.decode()

    try:
        handler.handle(body, signature)
    except InvalidSignatureError as e:
        raise BadRequestError("NG") from e

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    response_text = get_response_text(event.message.text)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response_text))
