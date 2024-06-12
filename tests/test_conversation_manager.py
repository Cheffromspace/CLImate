import unittest
from unittest.mock import patch

from conversation_manager import (
    invoke_conversation,
    generate_conversation_name,
    get_conversation_names,
    remove_last_interaction,
)


class TestConversationManager(unittest.TestCase):
    def setUp(self):
        # Set up any necessary test data or mocks
        pass

    def tearDown(self):
        # Clean up any resources or reset any state
        pass

    @patch("conversation_manager.get_current_conversation_file")
    @patch("conversation_manager.set_current_conversation_file")
    @patch("conversation_manager.save_conversation_history")
    @patch("conversation_manager.load_conversation_history")
    @patch("conversation_manager.invoke_anthropic_api")
    def test_invoke_conversation(
        self,
        mock_invoke_anthropic_api,
        mock_load_conversation_history,
        mock_save_conversation_history,
        mock_set_current_conversation_file,
        mock_get_current_conversation_file,
    ):
        # Set up the mock responses
        mock_response = "<filename>Test_conversation_name</filename>"
        mock_invoke_anthropic_api.return_value = mock_response
        mock_get_current_conversation_file.return_value = None
        mock_load_conversation_history.return_value = []

        # Test the invoke_conversation function
        message = "Hello, how are you?"
        role, response = invoke_conversation(message)

        # Assert the expected behavior
        self.assertEqual(role, "assistant")
        self.assertEqual(response, mock_response)

        # Assert that the mock API function was called with the correct arguments
        mock_invoke_anthropic_api.assert_called()
        mock_args = mock_invoke_anthropic_api.call_args
        self.assertIn({"role": "user", "content": message}, mock_args[0][0])

        # Assert that the file operation functions were called
        mock_get_current_conversation_file.assert_called_once()
        mock_set_current_conversation_file.assert_called_once()
        mock_save_conversation_history.assert_called()
        mock_load_conversation_history.assert_called_once()

    @patch("conversation_manager.invoke_anthropic_api")
    @patch("conversation_manager.format_conversation_title")
    @patch("conversation_manager.extract_response_text")
    def test_generate_conversation_name(
        self,
        mock_extract_response_text,
        mock_format_conversation_title,
        mock_invoke_anthropic_api,
    ):
        # Set up the mock responses
        mock_summary = "<filename>Test_conversation_name</filename>"
        mock_invoke_anthropic_api.return_value = mock_summary
        mock_extract_response_text.return_value = "Test_conversation_name"

        # Test the generate_conversation_name function
        first_message = "This is a test message."
        conversation_name = generate_conversation_name(first_message)

        # Assert the expected behavior
        expected_conversation_name = "Test_conversation_name"
        self.assertEqual(conversation_name, expected_conversation_name)

        # Assert that the mock API function was called with the correct arguments
        mock_invoke_anthropic_api.assert_called_once()
        mock_args = mock_invoke_anthropic_api.call_args
        self.assertIn({"role": "user", "content": first_message}, mock_args[0][0])

        # Assert that the mock extract_response_text function was called with the correct arguments
        mock_extract_response_text.assert_called_once_with(mock_summary, "filename")

        # Assert that the mock format_conversation_title function was called with the correct argument
        mock_format_conversation_title.assert_called_once_with("Test_conversation_name")

    @patch("conversation_manager.os.listdir")
    @patch("conversation_manager.load_user_config")
    def test_get_conversation_names(self, mock_load_user_config, mock_listdir):
        # Set up the mock return values
        mock_load_user_config.return_value = {
            "conversations_directory": "/path/to/conversations"
        }
        mock_listdir.return_value = [
            "conversation1.json",
            "conversation2.json",
            "not_a_conversation.txt",
        ]

        # Test the get_conversation_names function
        conversation_names = get_conversation_names()

        # Assert the expected behavior
        expected_conversation_names = ["conversation1", "conversation2"]
        self.assertEqual(conversation_names, expected_conversation_names)

        # Assert that the mock functions were called with the correct arguments
        mock_load_user_config.assert_called_once()
        mock_listdir.assert_called_once_with("/path/to/conversations")

    @patch("conversation_manager.get_current_conversation_file")
    @patch("conversation_manager.load_conversation_history")
    @patch("conversation_manager.save_conversation_history")
    def test_remove_last_interaction(
        self,
        mock_save_conversation_history,
        mock_load_conversation_history,
        mock_get_current_conversation_file,
    ):
        # Set up the mock return values
        mock_get_current_conversation_file.return_value = "current_conversation.json"
        mock_load_conversation_history.return_value = [
            {"role": "user", "content": "First message"},
            {"role": "assistant", "content": "First response"},
            {"role": "user", "content": "Second message"},
            {"role": "assistant", "content": "Second response"},
        ]

        # Test the remove_last_interaction function
        success = remove_last_interaction()

        # Assert the expected behavior
        self.assertTrue(success)
        mock_save_conversation_history.assert_called_once_with(
            [
                {"role": "user", "content": "First message"},
                {"role": "assistant", "content": "First response"},
            ]
        )

        # Test the case when there are fewer than two interactions
        mock_load_conversation_history.return_value = [
            {"role": "user", "content": "Only message"}
        ]
        success = remove_last_interaction()
        self.assertFalse(success)
        mock_save_conversation_history.assert_called_once()  # Ensure save_conversation_history is not called again

        # Test the case when there is no current conversation file
        mock_get_current_conversation_file.return_value = None
        success = remove_last_interaction()
        self.assertFalse(success)
        mock_save_conversation_history.assert_called_once()  # Ensure save_conversation_history is not called again


if __name__ == "__main__":
    unittest.main()
