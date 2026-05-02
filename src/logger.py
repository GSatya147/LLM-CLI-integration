from datetime import datetime
import json, os

OUTPUT_DIR: str = 'logs'

OUTPUT_FILE: str = f'{OUTPUT_DIR}/logs.jsonl'

class ResponseLogger:
    def __init__(self, fname):
        self.fname = fname

        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

    def log(self, status: str, prompt: str, i_tokens: int, reponse: str, o_tokens: int) -> None:
        log_entry: dict = {
            'timestamp': str(datetime.now().strftime(f"%H:%M:%S %Y")),
            'status': status,
            'input': prompt,
            'input tokens': i_tokens,
            'output': reponse,
            'output tokens': o_tokens
        }

        json_string: json = json.dumps(log_entry, indent=4)

        with open(self.fname, "a") as af:
            af.write(json_string)
            af.write('\n')  

if __name__== "__main__":
    obj = ResponseLogger(OUTPUT_FILE)
    obj.log('SUCCESS', 'hi', 1,"replying to hi" , 4)
