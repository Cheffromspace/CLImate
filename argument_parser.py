import argparse
import argcomplete
from system_prompts import SYSTEM_PROMPTS


def parse_args():
    parser = argparse.ArgumentParser(description="Anthropic CLI")
    subparsers = parser.add_subparsers(dest="command")

    chat_parser = subparsers.add_parser(
        "chat", help="Send a message to the AI assistant"
    )
    chat_group = chat_parser.add_mutually_exclusive_group(required=True)
    chat_group.add_argument("message", nargs="?", help="The message to send")
    chat_group.add_argument(
        "-l", "--list-personas", action="store_true", help="List all available personas"
    )
    chat_group.add_argument(
        "-r",
        "--remove-last",
        action="store_true",
        help="Remove the last interaction from the conversation history",
    )
    chat_parser.add_argument("-m", "--model", type=str, help="The AI model to use")
    chat_parser.add_argument(
        "-t", "--temperature", type=float, help="The temperature value for the AI model"
    )
    chat_parser.add_argument(
        "-p",
        "--persona",
        type=str,
        choices=list(SYSTEM_PROMPTS.keys()),
        help="The AI persona to use",
    )
    chat_parser.add_argument(
        "-d",
        "--conversations-directory",
        type=str,
        help="The directory to store conversation files",
    )
    chat_parser.add_argument(
        "-j", "--json", action="store_true", help="Output the result as JSON"
    )

    reset_parser = subparsers.add_parser("reset", help="Reset the conversation history")

    write_parser = subparsers.add_parser(
        "write", help="Write the conversation history to a file"
    )
    write_parser.add_argument(
        "-n", "--name", type=str, help="The name of the conversation"
    )
    write_parser.add_argument(
        "-d",
        "--directory",
        type=str,
        help="The directory to save the conversation file",
    )
    interactive_parser = subparsers.add_parser(
        "interactive", help="Start an interactive chat session"
    )
    interactive_parser.add_argument(
        "-i", "--interactive", type=str, help="interactive_mode"
    )

    history_parser = subparsers.add_parser(
        "history", help="Display the conversation history"
    )
    history_parser.add_argument(
        "-r",
        "--raw",
        action="store_true",
        help="Display the conversation history as raw text without formatting",
    )

    import_parser = subparsers.add_parser(
        "import", help="Import a conversation history from a file"
    )
    import_parser.add_argument(
        "conversation_name", type=str, help="The name of the conversation to import"
    )
    import_parser.add_argument(
        "-d",
        "--directory",
        type=str,
        help="The directory containing the conversation file",
    )

    argcomplete.autocomplete(parser)
    return parser.parse_args()
