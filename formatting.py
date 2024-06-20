from rich.console import Console
from rich.style import Style
from rich.syntax import Syntax
from rich.text import Text
from rich.progress import Progress
from rich.markdown import Markdown

console = Console()

title_style = Style(
    color="green",
    bold=True,
)
user_style = Style(color="magenta")
assistant_style = Style(color="#7dcfff")


def format_user_message(message):
    console.print()
    console.print("User:", style=user_style)
    console.print(Markdown(message, style=user_style, code_theme="ansi_dark"))


def format_assistant_message(message):
    lines = message.split("\n")
    in_code_block = False
    code_block_lines = []
    language = "python"
    formatted_lines = []

    for line in lines:
        if line.startswith("```"):
            if in_code_block:
                # End of code block
                code_block = "\n".join(code_block_lines)
                syntax = Syntax(
                    code_block,
                    language,
                    line_numbers=False,
                    word_wrap=True,
                    background_color="default",  # Set background color to default
                )
                formatted_lines.append("```\n")  # Add opening backticks
                formatted_lines.append(syntax)
                formatted_lines.append("```")  # Add closing backticks
                code_block_lines = []
                in_code_block = False
            else:
                # Start of code block
                in_code_block = True
                language = line[
                    3:
                ].strip()  # Extract the language from the code block delimiter
                if not language:
                    language = "python"
        else:
            if in_code_block:
                code_block_lines.append(line)
            else:
                # Format inline code
                formatted_line = Text()
                parts = line.split("`")
                for i, part in enumerate(parts):
                    if i % 2 == 0:
                        formatted_line.append(part)
                    else:
                        formatted_line.append(Text(part, style="bold yellow"))
                formatted_lines.append(formatted_line)
                formatted_lines.append("\n")  # Add a newline after each line of text

    console.print("Assistant:", style=assistant_style)
    for line in formatted_lines:
        if isinstance(line, Syntax):
            console.print(line, style=assistant_style)
        else:
            console.print(line, style=assistant_style, end="")
    console.print()  # Add a newline at the end


def format_conversation_title(title):
    console.print(f"Title: {title}", style=title_style)


def format_code_block(code, language):
    syntax = Syntax(code, language, line_numbers=True)
    console.print(syntax)


def format_progress(total, current, description):
    with Progress() as progress:
        task = progress.add_task(description, total=total)
        progress.update(task, completed=current)


def format_markdown(markdown):
    md = Markdown(markdown)
    console.print(md)


def format_image(image_path):
    with open(image_path, "r") as image_file:
        image = image_file.read()
    console.print(image)
