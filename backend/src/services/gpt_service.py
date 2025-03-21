"""Module providing calls to gpt api"""

import os
import requests
import json
from dotenv import load_dotenv
from .file_service import load_prompt_from_file

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
        response = requests.head(image_url, timeout=5)
        response.raise_for_status()
        content_length = response.headers.get("Content-Length")
        if content_length and int(content_length) > 20971520:
            raise ValueError("The image size is larger than 20 MB.")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Invalid or inaccessible image URL: {e}")


def create_prompt(description, image_base64=None, image_url=None):
    """Function for prompt generation"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    if image_base64 or image_url:
        template_path = os.path.join(base_dir, "templates", "image_prompt.txt")
    else:
        template_path = os.path.join(base_dir, "templates", "text_prompt.txt")

    prompt = load_prompt_from_file(template_path)
    prompt += "\n\nDescription:\n" + description

    messages = [
        {"role": "system", "content": "You are a creative assistant."},
        {"role": "user", "content": [{"type": "text", "text": prompt}]},
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

    data = {
        "temperature": 0.8,
        "top_p": 0.6,
        "max_tokens": 4000,
        "messages": messages,
    }

    try:
        response = requests.post(api_endpoint, headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()
        # Debugging
        print("Full Response Data:", response_data)

        if "choices" in response_data:
            generated_content = response_data["choices"][0]["message"]["content"]
            return generated_content
        else:
            raise ValueError("The response does not contain 'choices'")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to extract keywords: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Error parsing response: {e}") from e


def extract_keywords(image_base64=None, image_url=None):
    """Method for extracting keywords from reference image"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    template_path = os.path.join(base_dir, "templates", "keyword_prompt.txt")
    prompt = load_prompt_from_file(template_path)
    messages = [
        {"role": "system", "content": "You are a creative assistant."},
        {"role": "user", "content": [{"type": "text", "text": prompt}]},
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
    try:
        response = requests.post(api_endpoint, headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()
        # Debugging
        print("Full Response Data:", response_data)

        if "choices" in response_data:
            generated_content = response_data["choices"][0]["message"]["content"]
            extracted_data = json.loads(generated_content)
            keywords = extracted_data.get("keywords", [])
            return keywords
        raise ValueError("The response does not contain 'choices'")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to extract keywords: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Error parsing response: {e}") from e
