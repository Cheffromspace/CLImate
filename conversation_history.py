import os
import sys
import json
from user_config import load_user_config
from formatting import format_assistant_message, format_user_message

CONVERSATION_DIRECTORY = load_user_config()["conversations_directory"]
CURRENT_CONVERSATION_FILE = CONVERSATION_DIRECTORY + "current_conversation.txt"


def save_conversation_history(conversation_history):
    with open(CURRENT_CONVERSATION_FILE, "w") as file:
        json_string = json.dumps(conversation_history)
        file.write(json_string)


def load_conversation_history():
    try:
        with open(CURRENT_CONVERSATION_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def get_current_conversation_file():
    try:
        with open(CURRENT_CONVERSATION_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return None


def set_current_conversation_file(file_name):
    with open(CURRENT_CONVERSATION_FILE, "w") as file:
        file.write(file_name)


def reset_conversation():
    current_conversation_file = get_current_conversation_file()
    if current_conversation_file:
        set_current_conversation_file("")
    print("Conversation reset.", file=sys.stderr)


def display_conversation_history(raw=False):
    conversation_history = load_conversation_history()
    if conversation_history:
        for message in conversation_history:
            role = message["role"]
            content = message["content"]
            if not raw:
                if role == "assistant":
                    format_assistant_message(content)
                else:
                    format_user_message(content)
            else:
                print(f"{role}: {content}")


def import_conversation(conversation_name):
    conversation_file = f"{conversation_name}.json"
    conversation_path = os.path.join(CONVERSATION_DIRECTORY, conversation_file)

    if os.path.exists(conversation_path):
        set_current_conversation_file(conversation_file)
        return conversation_name
    else:
        return None
