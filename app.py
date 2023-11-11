import os
import json
from logging import getLogger

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from lib.llms import get_simple_response_by_bedrock


logger = getLogger(__name__)

configuration = Configuration(os.getenv("CHANNEL_ACCESS_TOKEN", ""))
handler = WebhookHandler(os.getenv("CHANNEL_SECRET", ""))


def bad_request(message=""):
    return {
        "statusCode": 400,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": message}),
    }


def ok():
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({}),
    }


def lambda_handler(event, context):
    signature = event["headers"]["X-Line-Signature"]
    body = event["body"]
    logger.info(f"body: {body}")

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.info("invalid signature error")
        return bad_request("invalid signature")
    return ok()


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    response_text = get_simple_response_by_bedrock(event.message.text)
    with ApiClient(Configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=response_text)],
            )
        )
