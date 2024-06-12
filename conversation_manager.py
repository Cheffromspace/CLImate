import os
from conversation_history import (
    save_conversation_history,
    load_conversation_history,
    get_current_conversation_file,
    set_current_conversation_file,
)
from formatting import format_conversation_title
from anthropic_api import invoke_anthropic_api
from user_config import load_user_config
from system_prompts import SYSTEM_PROMPTS
from utils import extract_response_text


def invoke_conversation(
    message,
    model=None,
    temperature=None,
    system_message=None,
    conversations_directory=None,
):
    current_conversation_file = get_current_conversation_file()

    if not current_conversation_file:
        conversation_name = generate_conversation_name(message)
        current_conversation_file = f"{conversation_name}.json"
        set_current_conversation_file(current_conversation_file)
        save_conversation_history([])

    user_config = load_user_config()
    model = model or user_config["model"]
    temperature = temperature or user_config["temperature"]
    system_message = system_message or SYSTEM_PROMPTS[user_config["persona"]]
    conversations_directory = (
        conversations_directory or user_config["conversations_directory"]
    )

    conversation_history = load_conversation_history()
    conversation_history.append({"role": "user", "content": message})

    assistant_response = invoke_anthropic_api(
        conversation_history, model, temperature, system_message
    )

    conversation_history.append({"role": "assistant", "content": assistant_response})

    save_conversation_history(conversation_history)

    return "assistant", assistant_response


def generate_conversation_name(first_message):
    conversation_history = [
        {
            "role": "user",
            "content": f"<first_user_message>\n{first_message}\n</first_user_message>\nRemember your system message. Output only the filename enclosed in filename tags.",
        }
    ]

    system_message = """
You will be provided with the first user message in a chat session with an LLM. We're going to save this conversation to the filesystem and we want to create a meaningful name so we can refrence it and continue a conversation later if we choose. Please create a short filename, 3-7 words maximum, that describes the user's query. Focus more on the user's query or issue 
than any supporting documentation or code.

<example_output>
<filename>guide_to_creating_README_for_project</filename>
</example_output>
<example_output>
  <filename>troubleshooting_a_broken_user_config_file</filename>
</example_output>
<example_output>
  <filename>requesting_interaction_analysis</filename>
</example_output>
<example_output>
  <filename>occams_razor_simplest_explanation_principle</filename>
</example_output>
<example_output>
  <filename>setting_up_local_webserver</filename><
</example_output>
<example_output>
  <filename>summarize_rich_library_documentation</filename>
</example_output>
<example_output>
  <filename>healthy_dinner_ideas</filename>
</example_output>
Your output should be only a filename enclosed in <filename>...</filename> tags.
    """

    content_text = invoke_anthropic_api(
        conversation_history,
        model="claude-3-haiku-20240307",
        temperature=1.0,
        system_message=system_message,
    )
    extracted_text = extract_response_text(content_text, "filename")

    truncated_message = extracted_text[:100]
    format_conversation_title(truncated_message)
    conversation_name = truncated_message.replace(" ", "_").replace(".", "")
    return conversation_name


def get_conversation_names():
    conversations_directory = load_user_config()["conversations_directory"]
    conversation_files = os.listdir(conversations_directory)
    conversation_names = [
        file_name[:-5]
        for file_name in conversation_files
        if file_name.endswith(".json")
    ]
    return conversation_names


def remove_last_interaction():
    current_conversation_file = get_current_conversation_file()
    if current_conversation_file:
        conversation_history = load_conversation_history()
        if len(conversation_history) >= 2:
            conversation_history = conversation_history[:-2]
            save_conversation_history(conversation_history)
            return True
        else:
            return False
    else:
        return False
