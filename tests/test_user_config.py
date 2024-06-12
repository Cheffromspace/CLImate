import unittest
from unittest.mock import patch, mock_open
import json
from pathlib import Path
from user_config import load_user_config


class TestUserConfig(unittest.TestCase):
    @patch("user_config.Path.home")
    def test_load_user_config_existing_file(self, mock_home):
        # Mock the home directory and the config file
        mock_home.return_value = Path("/path/to/home")
        config_data = {
            "model": "claude-3-opus-20240229",
            "temperature": 0.7,
            "persona": "default",
            "conversations_directory": "/path/to/home/conversations",
        }
        mock_file_data = json.dumps(config_data)
        with patch("builtins.open", mock_open(read_data=mock_file_data)):
            # Test loading user config from an existing file
            config = load_user_config()
            self.assertEqual(config, config_data)

    @patch("user_config.Path.home")
    def test_load_user_config_nonexistent_file(self, mock_home):
        # Mock the home directory and the config file
        mock_home.return_value = Path("/path/to/home")
        with patch("builtins.open", mock_open()) as mock_file:
            mock_file.side_effect = FileNotFoundError
            # Test loading user config from a nonexistent file
            config = load_user_config()
            expected_config = {
                "model": "claude-3-opus-20240229",
                "temperature": 0.7,
                "persona": "default",
                "conversations_directory": "/path/to/home/conversations",
            }
            self.assertEqual(config, expected_config)


if __name__ == "__main__":
    unittest.main()
