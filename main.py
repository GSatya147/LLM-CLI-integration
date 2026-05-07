from src.client import get_response
from src.costing import calculate_costing
from src.logger import ResponseLogger
from rich.console import Console

TOTAL_COST: float = 0.00
TOTAL_TOKENS: int = 0

STATUS = None

console = Console()
logger = ResponseLogger("logs.jsonl")

while True:
    try:
        print(
            f"""
        Welcome to local Gemini-3-flash preview
        {'='*50}
        1. Access Gemini-3-flash
        2. Check the tokens usage
        3. Check the cost
        4. Exit
        """
        )
        option = int(input("Select 1/2/3/4: "))

        if option == 1:
            while True:
                input_tokens: int = 0
                output_tokens: int = 0
                try:
                    print(f"{'-' * 100}")
                    user_msg = input(">> ")

                    full_response = ""

                    last_chunk = None
                    for chunk in get_response(user_prompt=user_msg):
                        if chunk.text:
                            console.print(chunk.text)
                            full_response += chunk.text
                        last_chunk = chunk

                    input_tokens = last_chunk.usage_metadata.prompt_token_count
                    output_tokens = last_chunk.usage_metadata.candidates_token_count

                    TOTAL_COST += calculate_costing(input_tokens, output_tokens)
                    TOTAL_TOKENS += last_chunk.usage_metadata.total_token_count

                    STATUS = "SUCCESS"

                except EnvironmentError as e:
                    STATUS = "ERROR"
                    print(e)

                except KeyboardInterrupt:
                    print("Have a nice day!")
                    break

                except Exception as e:
                    print(f"Error!: {e}")
                    STATUS = "ERROR"

                finally:
                    logger.log(
                        STATUS, user_msg, input_tokens, full_response, output_tokens
                    )

        elif option == 2:
            print(f"Total tokens usage: {TOTAL_TOKENS}")

        elif option == 3:
            print(f"Total cost: ${TOTAL_COST:.5f}")

        elif option == 4:
            break

        else:
            print("Please enter a valid option, 1/2/3/4")

    except KeyboardInterrupt:
        print("\nExiting...")
        break
