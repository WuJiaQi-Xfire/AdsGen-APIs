"""Module providing calls to gpt api"""

import os
import json
import requests
from dotenv import load_dotenv
from .file_service import load_prompt_from_file

# Load env variables
env_path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("AZURE_GPT_API_KEY")
api_endpoint = os.getenv("AZURE_GPT_API_ENDPOINT")

headers = {
    "Content-Type": "application/json",
    "api-key": api_key,
    "model": "gpt-4o-mini",
    "api-version": "2024-02-01",
}


def validate_image_url(image_url):
    """Function to validate image url"""
    try:
        response = requests.head(image_url, timeout=10)
        response.raise_for_status()
        content_length = response.headers.get("Content-Length")
        if content_length and int(content_length) > 20971520:
            raise ValueError("The image size is larger than 20 MB.")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Invalid or inaccessible image URL: {e}") from e


def create_message(content, image_url=None, image_base64=None):
    """Function to create messages for API requests."""
    messages = [
        {"role": "system", "content": "You are a creative assistant."},
        {"role": "user", "content": [{"type": "text", "text": content}]},
    ]

    if image_url:
        validate_image_url(image_url)
        messages[1]["content"].append(
            {"type": "image_url", "image_url": {"url": image_url, "detail": "high"}}
        )
    elif image_base64:
        messages[1]["content"].append(
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
            }
        )

    return messages


def make_api_call(data):
    """Function to make a POST request to the API."""
    try:
        response = requests.post(api_endpoint, headers=headers, json=data, timeout=25)
        response.raise_for_status()
        response_data = response.json()
        #print("Full Response Data:", response_data)  # Debugging

        if "choices" in response_data:
            return response_data["choices"][0]["message"]["content"]
        else:
            raise ValueError("The response does not contain 'choices'")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"API request failed: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Error processing response: {e}") from e


def create_prompt(description, image_base64=None, image_url=None):
    """Function for prompt generation"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    template_path = os.path.join(
        base_dir,
        "templates",
        "image_prompt.txt" if image_base64 or image_url else "text_prompt.txt",
    )

    prompt = load_prompt_from_file(template_path) + "\n\nDescription:\n" + description
    messages = create_message(prompt, image_url, image_base64)

    data = {
        "temperature": 0.8,
        "top_p": 0.6,
        "max_tokens": 4000,
        "messages": messages,
    }

    return make_api_call(data)


def extract_keywords(image_base64=None, image_url=None):
    """Method for extracting keywords from reference image."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    template_path = os.path.join(base_dir, "templates", "keyword_prompt.txt")
    prompt = load_prompt_from_file(template_path)

    messages = create_message(prompt, image_url, image_base64)

    data = {
        "temperature": 0.8,
        "top_p": 0.6,
        "max_tokens": 4000,
        "messages": messages,
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "structured_response",
                "schema": {
                    "type": "object",
                    "properties": {
                        "keywords": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["keywords"],
                    "additionalProperties": False,
                },
                "strict": True,
            },
        },
    }

    generated_content = make_api_call(data)
    extracted_data = json.loads(generated_content)
    return extracted_data.get("keywords", [])
