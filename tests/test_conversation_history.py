import unittest
from unittest.mock import patch, mock_open
import json
from conversation_history import (
    save_conversation_history,
    load_conversation_history,
    get_current_conversation_file,
    set_current_conversation_file,
    display_conversation_history,
    import_conversation,
)


class TestConversationHistory(unittest.TestCase):
    @patch(
        "conversation_history.CURRENT_CONVERSATION_FILE",
        "test_conversations/current_conversation.txt",
    )
    @patch("builtins.open", new_callable=mock_open)
    def test_save_conversation_history(self, mock_file):
        conversation_history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
        ]
        json_string = json.dumps(conversation_history)
        save_conversation_history(conversation_history)
        mock_file.assert_called_once_with(
            "test_conversations/current_conversation.txt", "w"
        )
        mock_file().write.assert_called_once_with(json_string)

    @patch(
        "conversation_history.CURRENT_CONVERSATION_FILE",
        "test_conversations/current_conversation.txt",
    )
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='[{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi there!"}]',
    )
    def test_load_conversation_history(self, mock_file):
        conversation_history = load_conversation_history()
        expected_history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
        ]
        self.assertEqual(conversation_history, expected_history)
        mock_file.assert_called_once_with(
            "test_conversations/current_conversation.txt", "r"
        )

    @patch(
        "conversation_history.CURRENT_CONVERSATION_FILE",
        "test_conversations/current_conversation.txt",
    )
    @patch("builtins.open", new_callable=mock_open)
    def test_load_conversation_history_file_not_found(self, mock_file):
        mock_file.side_effect = FileNotFoundError
        conversation_history = load_conversation_history()
        self.assertEqual(conversation_history, [])

    @patch(
        "conversation_history.CURRENT_CONVERSATION_FILE",
        "test_conversations/current_conversation.txt",
    )
    @patch("builtins.open", new_callable=mock_open, read_data="test_conversation.json")
    def test_get_current_conversation_file(self, mock_file):
        current_file = get_current_conversation_file()
        self.assertEqual(current_file, "test_conversation.json")
        mock_file.assert_called_once_with(
            "test_conversations/current_conversation.txt", "r"
        )

    @patch(
        "conversation_history.CURRENT_CONVERSATION_FILE",
        "test_conversations/current_conversation.txt",
    )
    @patch("builtins.open", new_callable=mock_open)
    def test_set_current_conversation_file(self, mock_file):
        set_current_conversation_file("new_conversation.json")
        mock_file.assert_called_once_with(
            "test_conversations/current_conversation.txt", "w"
        )
        mock_file().write.assert_called_once_with("new_conversation.json")

    @patch("conversation_history.load_conversation_history")
    @patch("conversation_history.format_assistant_message")
    @patch("conversation_history.format_user_message")
    def test_display_conversation_history(
        self,
        mock_format_user_message,
        mock_format_assistant_message,
        mock_load_conversation_history,
    ):
        mock_load_conversation_history.return_value = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
        ]
        display_conversation_history()
        mock_format_user_message.assert_called_once_with("Hello")
        mock_format_assistant_message.assert_called_once_with("Hi there!")

    @patch("conversation_history.load_conversation_history")
    @patch("builtins.print")
    def test_display_conversation_history_raw(
        self, mock_print, mock_load_conversation_history
    ):
        mock_load_conversation_history.return_value = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
        ]
        display_conversation_history(raw=True)
        mock_print.assert_any_call("user: Hello")
        mock_print.assert_any_call("assistant: Hi there!")

    @patch("conversation_history.set_current_conversation_file")
    @patch("os.path.exists")
    def test_import_conversation(self, mock_exists, mock_set_current_conversation_file):
        mock_exists.return_value = True
        conversation_name = import_conversation("test_conversation")
        self.assertEqual(conversation_name, "test_conversation")
        mock_set_current_conversation_file.assert_called_once_with(
            "test_conversation.json"
        )

    @patch("os.path.exists")
    def test_import_conversation_not_found(self, mock_exists):
        mock_exists.return_value = False
        conversation_name = import_conversation("nonexistent_conversation")
        self.assertIsNone(conversation_name)


if __name__ == "__main__":
    unittest.main()
