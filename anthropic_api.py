import os
import anthropic
from time import sleep
import sys
from logging import getLogger

logger = getLogger(__name__)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")


def invoke_anthropic_api(
    conversation_history, model, temperature, system_message, max_retries=3
):
    client = anthropic.Client(api_key=ANTHROPIC_API_KEY)

    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                model=model,
                messages=conversation_history,
                max_tokens=4096,
                temperature=temperature,
                system=system_message,
            )
            content_text = " ".join(block.text for block in response.content)
            return content_text
        except anthropic.BadRequestError as e:
            logger.error(f"Bad request error: {str(e)}")
            raise e
        except anthropic.AuthenticationError as e:
            logger.error(f"Authentication error: {str(e)}")
            raise e
        except anthropic.PermissionDeniedError as e:
            logger.error(f"Permission denied error: {str(e)}")
            raise e
        except anthropic.RateLimitError as e:
            retry_after = int(e.response.headers.get("retry-after"))
            if retry_after:
                if attempt < max_retries - 1:
                    wait_message = f"Rate limit exceeded. Retrying in {retry_after} seconds. Attempt {attempt + 1}/{max_retries}"
                    print(wait_message, file=sys.stderr)
                    logger.warning(wait_message)
                    sleep(retry_after)
                else:
                    logger.error("Rate limit exceeded. Max retries reached.")
                    raise e
            else:
                logger.error("Rate limit exceeded. Retry information not available.")
                raise e
        except anthropic.APIError as e:
            logger.error(f"Unexpected API error: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise e
