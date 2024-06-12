import json
from pathlib import Path

CONFIG_FILE = ".chat_config.json"


def load_user_config():
    home_dir = Path(Path.home())  # Convert the string to a Path object
    config_file = home_dir / CONFIG_FILE

    if config_file.exists():
        with open(config_file, "r") as file:
            return json.load(file)
    else:
        return {
            "model": "claude-3-opus-20240229",
            "temperature": 0.7,
            "persona": "default",
            "conversations_directory": str(home_dir / "conversations"),
        }
