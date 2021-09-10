import json
import os
import boto3

# Core handler addresses messages and devlivers them to LEX
def lambda_handler(event, context):
    user_id, text = get_info_from_request(event)
    if user_id is None or text is None:
        return error_handler("No text or user_id information.")
    response = error_handler("Lex connection fail.")

    chatbot_text = get_chatbot(user_id, text)
    if chatbot_text is not None:
        response = message_handler(chatbot_text, user_id)
    return response


def get_chatbot(user_id, text):
    client = boto3.client('lex-runtime')
    bot_response = client.post_text(
        botName='SuggestRestaurant',
        botAlias="$LATEST",
        userId='AWS_Admin',
        inputText=text
    )
    if not isinstance(bot_response, dict) or 'message' not in bot_response:
        return None
    return bot_response['message']


def get_info_from_request(event):
    if "messages" not in event or not isinstance(event["messages"], list) or len(event["messages"]) == 0:
        print("no message available.")
        return None, None
    message = event["messages"][0]

    if "unconstructed" not in message or "text" not in message["unconstructed"] or "user_id" not in message[
        "unconstructed"]:
        print("incorrect format.")
        return None, None

    return message["unconstructed"]["user_id"], message["unconstructed"]["text"]


def error_handler(text):
    response = {
        "status code": 200,
        "body": {
            "messages": [
                {
                    "type": "chotbot_message",
                    "unconstructed": {
                        "user_id": None,
                        "text": text,
                    }
                }]
        }
    }
    return response


def message_handler(text, user_id):
    response = {
        "status code": 200,
        "body": {
            "messages": [
                {
                    "type": "chotbot_message",
                    "unconstructed": {
                        "user_id": user_id,
                        "text": text,
                    }
                }]
        }
    }
    return response

