from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from conversation_manager import (
    invoke_conversation,
    remove_last_interaction,
)
from conversation_history import reset_conversation
from formatting import format_user_message, format_assistant_message


def interactive_chat():
    print(
        "Entering interactive chat mode. Type 'quit' or 'exit' to end the conversation."
    )

    session = PromptSession(
        auto_suggest=AutoSuggestFromHistory(),
        completer=WordCompleter(["reset", "undo", "quit", "exit"]),
    )

    while True:
        try:
            user_input = session.prompt("User: ")

            if user_input.lower() in ["quit", "exit"]:
                print("Exiting interactive chat mode.")
                break

            if user_input.lower() == "reset":
                reset_conversation()
                print("Conversation history has been reset.")
                continue

            if user_input.lower() == "undo":
                success = remove_last_interaction()
                if success:
                    print("Last interaction removed from the conversation history.")
                else:
                    print("No interactions to remove from the conversation history.")
                continue

            role, response = invoke_conversation(user_input)

            if role == "assistant":
                format_assistant_message(response)
            else:
                format_user_message(response)

        except KeyboardInterrupt:
            print("\nExiting interactive chat mode.")
            break


if __name__ == "__main__":
    from argument_parser import parse_args

    args = parse_args()
    interactive_chat()
