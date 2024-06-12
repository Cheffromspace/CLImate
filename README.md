# CLImate

CLImate is a Command Line Interface for Collaborative Language Interaction with Large Language Models. It provides an interactive chat experience with AI models, allowing users to engage in conversations, manage conversation history, and customize the AI's persona.

## Features

- Interactive chat mode for real-time conversations with the AI
- Support for different AI models and temperature settings
- Customizable AI personas for different conversation styles
- Conversation history management (save, load, reset)
- Importing and exporting conversation files
- Formatted output and syntax hilighting for improved readability

![image](https://github.com/Cheffromspace/CLImate/assets/21370528/a4a626e1-e461-4a68-8767-75752a92a868)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Cheffromspace/CLImate.git
   ```

2. Navigate to the project directory:
   ```
   cd CLImate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the Anthropic API key:
   - Sign up for an Anthropic API key at [https://www.anthropic.com](https://www.anthropic.com)
   - Set the `ANTHROPIC_API_KEY` environment variable with your API key:
  ```
  export ANTHROPIC_API_KEY=your_api_key_here
  ```

## Usage

To start an interactive chat session:
```
python climate.py interactive
```

To send a single message to the AI:
```
python climate.py chat "Your message here"
```

To reset the conversation history:
```
python climate.py reset
```

To display the conversation history:
```
python climate.py history
```

To import a conversation file:
```
python climate.py import conversation_name
```

For more options and details, use the `--help` flag:
```
python climate.py --help
```

## Configuration

CLImate uses a configuration file (`.chat_config.json`) to store user preferences. The default configuration is:
```json
{
  "model": "claude-3-opus-20240229",
  "temperature": 0.7,
  "persona": "default",
  "conversations_directory": "~/conversations"
}
```

You can modify these settings by editing the `.chat_config.json` file in your home directory.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request. Make sure to follow the existing code style and include tests for any new features or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Anthropic](https://www.anthropic.com) for providing the AI models and API
- [Rich](https://github.com/Textualize/rich) for the formatting and styling of the CLI output
