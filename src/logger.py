from datetime import datetime
import json
import os

OUTPUT_DIR: str = 'logs'

OUTPUT_FILE: str = f'{OUTPUT_DIR}/'

class ResponseLogger:
    def __init__(self, fname):
        self.fname = fname

        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

    def log(self, status: str, prompt: str, i_tokens: int, response: str, o_tokens: int) -> None:
        log_entry: dict = {
            'timestamp': str(datetime.now().strftime("%H:%M:%S %Y")),
            'status': status,
            'input': prompt,
            'input tokens': i_tokens,
            'output': response,
            'output tokens': o_tokens
        }

        json_string: str = json.dumps(log_entry)

        with open(os.path.join(OUTPUT_FILE, self.fname), "a") as af:
            af.write(json_string)
            af.write('\n')  

if __name__== "__main__":
    obj = ResponseLogger(OUTPUT_FILE)
    obj.log('SUCCESS', 'hi', 1,"replying to hi" , 4)
