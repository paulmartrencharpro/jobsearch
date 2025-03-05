from huggingface_hub import login, InferenceClient

import os

login(os.getenv('HF'))

def call_ai(prompt, json_mode):
    client = InferenceClient("mistralai/Mistral-Small-24B-Instruct-2501")

    extra_param = {}
    if json_mode:
        extra_param = { "response_format" : {"type": "json",
    "value": {
        "properties": {
            "company_description": {"type": "string"},
            "position_summary": {"type": "string"},
            "language_requirements": {"type": "string"},
            "experience_requirements": {"type": "string"},
            "is_an_internship": {"type": "boolean"},
            "salary_range": {"type": "string"},
            "should_apply": {"type": "boolean"},
        },
        "required": ["company_description", "position_summary", "experience_requirements", "language_requirements", "is_an_internship", "salary_range", "should_apply"],
    }} }

    chat_response = client.chat_completion(
        messages = [
            { "role" : "system", "content" : "You are a helpful assistant that generates JSON"},
            {
                "role": "user",
                "content": prompt,
            },
        ],
        max_tokens=1500,
        **extra_param
    )

    return chat_response.choices[0].message.content