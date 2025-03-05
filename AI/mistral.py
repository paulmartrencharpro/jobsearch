from mistralai import Mistral, SDKError
from time import sleep
import os

models = ["mistral-small-latest", "open-mistral-nemo"]

import random
def get_model():
    return random.choice(models)

def call_ai(prompt, json_mode):
    try:
        return _call_ai(prompt, json_mode)
    except SDKError as e:
        #Wait, then try again once
        sleep(11)
        return _call_ai(prompt, json_mode)
    except Exception as e:
        # Throw the error if it's not an SDKError
        raise

def _call_ai(prompt, json_mode):
    sleep(1.1)
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