from mistralai import Mistral, SDKError
from time import sleep
import os

def get_model():
    return "mistral-small-latest"

def call_ai(prompt, json_mode):
    try:
        sleep(0.1)
        return _call_ai(prompt, json_mode)
    except SDKError as e:
        #Wait, then try again once
        print(f"failed once - {e.message}")
        sleep(5)
        try:
            return _call_ai(prompt, json_mode)
        except SDKError as e:
            #Wait, then try again once
            print(f"failed twice - {e.message}")
            sleep(10)
            return _call_ai(prompt, json_mode)
    except Exception as e:
        # Throw the error if it's not an SDKError
        raise

import time
from datetime import datetime

def log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{timestamp} - {message}")

def _call_ai(prompt, json_mode):
    start = time.perf_counter()
    result = __call_ai(prompt, json_mode)
    duration = time.perf_counter() - start
    log(f"AI call took {duration:.4f} seconds")
    return result

def __call_ai(prompt, json_mode):
    client = Mistral(api_key=os.getenv('MISTRAL_KEY'))

    extra_param = {}
    if json_mode:
        extra_param = { "response_format" : {"type": "json_object"} }

    chat_response = client.chat.complete(
        model = get_model(),
        messages = [
            {
                "role": "user",
                "content": prompt,
            },
        ],
        **extra_param
    )
    
    return chat_response.choices[0].message.content