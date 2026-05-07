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
import time
from google import genai
from google.genai import types, errors
from dotenv import load_dotenv

MODEL_ID = "gemini-3-flash-preview"
MAX_RETRIES = 3

SYSTEM_PROMPT = 'You are a finance advisor'

load_dotenv()
your_api_key = os.getenv("GEMINI_API_key")
if not your_api_key:
    raise EnvironmentError("Gemini Key not set, Check your .env file")

def get_response(user_prompt, system_instr = SYSTEM_PROMPT):
        client = genai.Client(
            api_key = your_api_key,
            http_options=types.HttpOptions(
                timeout = 60000,
                retry_options=types.HttpRetryOptions(
                    attempts=3,              # Maximum 5 attempts (including original)
                    initial_delay=1.0,       # 1 second initial delay
                    max_delay=30.0,          # Maximum 60 seconds between retries
                )
            )
        )

        for attempt in range(MAX_RETRIES):
                try: 
                    response_stream = client.models.generate_content_stream(
                        model = MODEL_ID, 
                        contents = user_prompt,
                        config = types.GenerateContentConfig(
                            system_instruction = system_instr
                        )
                    )

                    for chunk in response_stream:
                        yield chunk
        
                except errors.ClientError as e: # explore other codes like 400, 401, 404
                    if e.code == 429:
                        wait_time = 2 ** attempt
                        print(f"Rate limited. waiting {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    else:
                         print(f"Client error: {e.message}")
                         break

                except errors.ServerError as e:
                    print(f"Server error on attempt {attempt + 1}: {e.message} ")
                    if attempt < MAX_RETRIES - 1:
                        time.sleep(2 ** attempt)
                        continue
                    else:
                        print("Exhausted retries!")
                        break

                except Exception as e:
                    print(f"Unexpected error: {e}")
        