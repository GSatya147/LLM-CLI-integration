"""
load env
get api key → if None, raise immediately

initialise client with api key

function get_response(system_prompt, user_message):
    try:
        call API with:
            - model name
            - system prompt
            - user message
            - streaming enabled
        return the stream
    except AuthError → "bad API key"
    except RateLimitError → "slow down, retry"
    except ConnectionError → "network issue"
"""

import os
from google import genai
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

load_dotenv()

your_api_key = os.getenv("GEMINI_API_key")
if not your_api_key:
    raise EnvironmentError("Gemini Key not set, Check your .env file")

client = genai.Client(api_key = your_api_key)

prompt = "Explain how AI works in 200 words"

response_stream = client.models.generate_content_stream(
    model = "gemini-3-flash-preview", 
    contents = prompt
)

console = Console()
for chunk in response_stream:
    if chunk.text:
        console.print(Markdown(chunk.text))