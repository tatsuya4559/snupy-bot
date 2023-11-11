import os
from logging import getLogger

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
)

from lib.llms import get_simple_response_by_bedrock


logger = getLogger(__name__)

line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN", ""))
handler = WebhookHandler(os.getenv("CHANNEL_SECRET", ""))


def lambda_handler(event, context):
    signature = event["headers"]["X-Line-Signature"]
    print(signature)
    body = event["body"]
    logger.info(f"body: {body}")

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": {}
    }


"""
@app.route("/api/line/callback", methods=["POST"])
def callback():
    request = app.current_request
    signature = request.headers["X-Line-Signature"]
    body = request.raw_body.decode()
    logger.info(f"body: {body}")

    try:
        handler.handle(body, signature)
    except InvalidSignatureError as e:
        logger.info("invalid signature error")
        raise BadRequestError("NG") from e

    return "OK"
"""


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    response_text = get_simple_response_by_bedrock(event.message.text)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response_text))
