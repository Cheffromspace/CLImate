from rich.console import Console
from rich.table import Table
from conversation_history import (
    reset_conversation,
    display_conversation_history,
    import_conversation,
)

from formatting import format_user_message, format_assistant_message
from conversation_manager import (
    invoke_conversation,
    remove_last_interaction,
)
from system_prompts import SYSTEM_PROMPTS
from argument_parser import parse_args
from interactive import interactive_chat


console = Console()


def main():
    args = parse_args()
    console = Console()
    if args.command == "chat":
        if args.list_personas:
            table = Table(title="Available Personas")
            table.add_column("Persona", style="cyan")
            table.add_column("Description", style="magenta")

            for persona, description in SYSTEM_PROMPTS.items():
                table.add_row(persona, description)

            console.print(table)
        elif args.remove_last:
            success = remove_last_interaction()
            if success:
                console.print("Last interaction removed from the conversation history.")
            else:
                console.print(
                    "No interactions to remove from the conversation history."
                )
        else:
            system_message = SYSTEM_PROMPTS.get(args.persona, SYSTEM_PROMPTS["default"])
            role, response = invoke_conversation(
                args.message,
                args.model,
                args.temperature,
                system_message,
                args.conversations_directory,
            )
            if role == "assistant":
                format_assistant_message(response)
            else:
                format_user_message(response)

    elif args.command == "reset":
        reset_conversation()

    elif args.command == "history":
        console.print("Conversation history:")
        display_conversation_history(args.raw)

    elif args.command == "import":
        conversation_name = args.conversation_name
        imported_conversation = import_conversation(conversation_name)
        if imported_conversation:
            console.print(f"Imported conversation: {imported_conversation}")
        else:
            console.print(f"Conversation file not found: {conversation_name}.json")
    elif args.command == "interactive":
        interactive_chat()


if __name__ == "__main__":
    main()
