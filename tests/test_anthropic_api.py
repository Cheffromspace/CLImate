import unittest
from unittest.mock import patch, MagicMock
import anthropic
from anthropic_api import invoke_anthropic_api


class TestAnthropicAPI(unittest.TestCase):
    def setUp(self):
        self.conversation_history = [
            {"role": "user", "content": "What is the capital of France?"},
            {"role": "assistant", "content": "The capital of France is Paris."},
            {"role": "user", "content": "Can you tell me more about Paris?"},
        ]
        self.model = "claude-v1"
        self.temperature = 0.7
        self.system_message = "You are a helpful assistant."

    @patch("anthropic.Client")
    def test_successful_api_call(self, mock_client):
        mock_response = MagicMock()
        mock_response.content = [
            MagicMock(
                text="Paris is the largest city and capital of France. It is known for its iconic landmarks like the Eiffel Tower, Louvre Museum, and Notre-Dame Cathedral. The city is also renowned for its art, fashion, cuisine, and rich history."
            )
        ]
        mock_client.return_value.messages.create.return_value = mock_response

        result = invoke_anthropic_api(
            self.conversation_history, self.model, self.temperature, self.system_message
        )

        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertIn("Paris is the largest city and capital of France.", str(result))

    @patch("anthropic.Client")
    def test_bad_request_error(self, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"error": "Bad request"}
        mock_client.return_value.messages.create.side_effect = (
            anthropic.BadRequestError(
                message="Bad request", response=mock_response, body="Bad request"
            )
        )

        with self.assertLogs(level="ERROR") as log_records:
            with self.assertRaises(
                anthropic.BadRequestError, msg="Expected BadRequestError to be raised"
            ):
                invoke_anthropic_api(
                    self.conversation_history,
                    self.model,
                    self.temperature,
                    self.system_message,
                )

        self.assertTrue(
            any(
                "Bad request error: Bad request" in record.getMessage()
                for record in log_records.records
            )
        )

    @patch("anthropic.Client")
    def test_authentication_error(self, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"error": "Authentication failed"}
        mock_client.return_value.messages.create.side_effect = (
            anthropic.AuthenticationError(
                message="Authentication failed",
                response=mock_response,
                body="Authentication failed",
            )
        )

        with self.assertLogs(level="ERROR") as log_records:
            with self.assertRaises(
                anthropic.AuthenticationError,
                msg="Expected AuthenticationError to be raised",
            ):
                invoke_anthropic_api(
                    self.conversation_history,
                    self.model,
                    self.temperature,
                    self.system_message,
                )

        self.assertTrue(
            any(
                "Authentication error: Authentication failed" in record.getMessage()
                for record in log_records.records
            )
        )

    @patch("anthropic.Client")
    def test_rate_limit_error_with_retry(self, mock_client):
        mock_response_rate_limit = MagicMock()
        mock_response_rate_limit.status_code = 429
        mock_response_rate_limit.json.return_value = {"error": "Rate limit exceeded"}
        mock_response_rate_limit.headers = {"retry-after": "1"}
        mock_response_success = MagicMock()
        mock_response_success.content = [
            MagicMock(text="Paris is a beautiful city with a rich cultural heritage.")
        ]
        mock_client.return_value.messages.create.side_effect = [
            anthropic.RateLimitError(
                message="Rate limit exceeded",
                response=mock_response_rate_limit,
                body="Rate limit exceeded",
            ),
            mock_response_success,
        ]

        with self.assertLogs(level="WARNING") as log_records:
            result = invoke_anthropic_api(
                self.conversation_history,
                self.model,
                self.temperature,
                self.system_message,
            )

        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertIn(
            "Paris is a beautiful city with a rich cultural heritage.", str(result)
        )
        self.assertTrue(
            any(
                "Rate limit exceeded. Retrying in 1 seconds. Attempt 1/3"
                in record.getMessage()
                for record in log_records.records
            )
        )

    @patch("anthropic.Client")
    def test_rate_limit_error_max_retries_exceeded(self, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.json.return_value = {"error": "Rate limit exceeded"}
        mock_response.headers = {"retry-after": "1"}
        mock_client.return_value.messages.create.side_effect = anthropic.RateLimitError(
            message="Rate limit exceeded",
            response=mock_response,
            body="Rate limit exceeded",
        )

        with self.assertLogs(level="ERROR") as log_records:
            with self.assertRaises(
                anthropic.RateLimitError,
                msg="Expected RateLimitError to be raised after max retries",
            ):
                invoke_anthropic_api(
                    self.conversation_history,
                    self.model,
                    self.temperature,
                    self.system_message,
                    max_retries=3,
                )

        self.assertTrue(
            any(
                "Rate limit exceeded. Max retries reached." in record.getMessage()
                for record in log_records.records
            )
        )


if __name__ == "__main__":
    unittest.main()
