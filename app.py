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


def bad_request(message=""):
    return {
        "statusCode": 400,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": {
            "message": message
        }
    }

def ok():
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": {}
    }


def lambda_handler(event, context):
    headers = event["headers"]
    signature = headers.get("X-Line-Signature")
    if not signature:
        return bad_request("signature not found")
    body = event["body"]
    logger.info(f"body: {body}")

    try:
        handler.handle(body, signature)
    except InvalidSignatureError as e:
        logger.info("invalid signature error")
        return bad_request("invalid signature")
    return ok()


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    response_text = get_simple_response_by_bedrock(event.message.text)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response_text))
