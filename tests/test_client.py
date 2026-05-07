from unittest.mock import MagicMock, patch
from src.client import get_response
import pytest


def test_raises_when_api_key_missing():
    with patch("src.client.your_api_key", None):
        with pytest.raises(EnvironmentError):
            list(get_response("test_prompt"))


def test_get_response_yields_chunks():
    fake_chunk = MagicMock()
    fake_chunk.text = "Hello from fake Gemini"

    with patch("src.client.genai.Client") as mock_client:
        mock_instance = mock_client.return_value
        mock_instance.models.generate_content_stream.return_value = [fake_chunk]

        chunks = list(get_response("test prompt"))

    assert len(chunks) == 1  # cus successful run only yields 1 time
    assert chunks[0].text == "Hello from fake Gemini"
