from unittest.mock import MagicMock, patch
from src.client import get_response
from google.genai import errors
import pytest


def test_raises_when_api_key_missing():
    with patch("src.client.your_api_key", None):
        with pytest.raises(EnvironmentError):
            list(get_response("test_prompt"))


def test_get_response_yields_chunks():
    fake_chunk = MagicMock()
    fake_chunk.text = "Hello from fake Gemini"

    with patch("src.client.your_api_key", "fake-key"):
        with patch("src.client.genai.Client") as mock_client:
            mock_instance = mock_client.return_value
            mock_instance.models.generate_content_stream.return_value = [fake_chunk]

            chunks = list(get_response("test prompt"))

    assert len(chunks) == 1  # cus successful run only yields 1 time
    assert chunks[0].text == "Hello from fake Gemini"


def test_retries_on_rate_limit():
    fake_chunk = MagicMock()
    fake_chunk.text = "success after retry"

    rate_limit_error = errors.ClientError(429, {"error": "rate limited"})

    with patch("src.client.your_api_key", "fake-key"):
        with patch("src.client.time.sleep") as mock_sleep:
            with patch("src.client.genai.Client") as mock_client:
                mock_instance = mock_client.return_value
                mock_instance.models.generate_content_stream.side_effect = (
                    [  # Multiple values for multiple iterations
                        rate_limit_error,
                        [fake_chunk],
                    ]
                )

                chunks = list(get_response("test prompt"))

    assert len(chunks) == 1
    mock_sleep.assert_called_once_with(1)


def test_exhausts_retries_on_repeated_rate_limit():
    rate_limit_error = errors.ClientError(429, {"error": "rate limited"})

    with patch("src.client.your_api_key", "fake-key"):
        with patch("src.client.time.sleep"):
            with patch("src.client.genai.Client") as mock_client:
                mock_instance = mock_client.return_value
                mock_instance.models.generate_content_stream.side_effect = [
                    rate_limit_error,
                    rate_limit_error,
                    rate_limit_error,
                ]

                chunks = list(get_response("test prompt"))

    assert len(chunks) == 0


def test_retries_on_server_error():
    fake_chunk = MagicMock()
    fake_chunk.text = "success after server error"

    server_error = errors.ServerError(500, {"error": "server error"})

    with patch("src.client.your_api_key", "fake-key"):
        with patch("src.client.time.sleep"):
            with patch("src.client.genai.Client") as mock_client:
                mock_instance = mock_client.return_value
                mock_instance.models.generate_content_stream.side_effect = [
                    server_error,
                    [fake_chunk],
                ]

                chunks = list(get_response("test prompt"))

    assert len(chunks) == 1


def test_handles_unexpected_exception():
    with patch("src.client.your_api_key", "fake-key"):
        with patch("src.client.time.sleep"):
            with patch("src.client.genai.Client") as mock_client:
                mock_instance = mock_client.return_value
                mock_instance.models.generate_content_stream.side_effect = [
                    ValueError("something unexpected"),
                ]

                chunks = list(get_response("test prompt"))

    assert len(chunks) == 0
