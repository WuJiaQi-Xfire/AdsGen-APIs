"""Module providing calls to gpt api"""

import os
import json
from typing import Optional, Dict, Any, Union, List
import requests
from dotenv import load_dotenv
from src.services.file_service import file_service
from src.services.llm_service import llm_service

# Load env variables
env_path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(dotenv_path=env_path)


class GPTService:
    def __init__(self):
        self.api_key = os.getenv("AZURE_GPT_API_KEY")
        self.api_endpoint = os.getenv("AZURE_GPT_API_ENDPOINT")
        self.headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key,
            "model": "gpt-4o-mini",
            "api-version": "2024-02-01",
        }

    def make_api_call(self, data: Dict[str, Any]) -> Union[str, Dict[str, Any]]:
        """Make API call to GPT service."""
        try:
            response = requests.post(
                self.api_endpoint, headers=self.headers, json=data, timeout=25
            )
            response.raise_for_status()
            response_data = response.json()

            if "choices" not in response_data:
                raise ValueError("The response does not contain 'choices'")

            return response_data["choices"][0]["message"]["content"]

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Error processing response: {e}") from e

    def generate_with_template(
        self,
        description: str,
        template_name: str,
        image_base64: Optional[str] = None,
        image_url: Optional[str] = None,
        response_format: Optional[Dict[str, Any]] = None,
    ) -> Union[str, Dict[str, Any]]:
        """
        Generate content using a template with optional image input.
        """
        # Load template
        base_dir = os.path.dirname(os.path.dirname(__file__))
        template_path = os.path.join(base_dir, "instructions", template_name)
        prompt = file_service.load_prompt_from_file(template_path)

        # Add description if provided
        if description:
            prompt += "\n\nDescription:\n" + description

        # Create messages
        messages = llm_service.create_message(prompt, image_url, image_base64)

        # Prepare request data
        data = llm_service.prepare_request_data(messages, response_format)

        # Make API call
        return self.make_api_call(data)

    def create_prompt(
        self,
        description: str,
        image_base64: Optional[str] = None,
        image_url: Optional[str] = None,
    ) -> str:
        """Generate prompt with optional image."""
        template_name = (
            "image_prompt.txt" if (image_base64 or image_url) else "text_prompt.txt"
        )
        return self.generate_with_template(
            description, template_name, image_base64, image_url
        )

    def generate_with_prompt(
        self,
        description: str,
        response_format: Optional[Dict[str, Any]] = None,
    ) -> Union[str, Dict[str, Any]]:
        """
        Generate image prompt with template prompt
        """
        # Use the description directly as the prompt
        prompt = description

        # Create messages
        messages = llm_service.create_message(prompt)

        # Prepare request data
        data = llm_service.prepare_request_data(messages, response_format)

        # Make API call
        return self.make_api_call(data)

    def extract_keywords(
        self, image_base64: Optional[str] = None, image_url: Optional[str] = None
    ) -> List[str]:
        """Extract keywords from image."""
        json_schema = {
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
        }

        response = self.generate_with_template(
            description="",
            template_name="keyword_prompt.txt",
            image_base64=image_base64,
            image_url=image_url,
            response_format=json_schema,
        )

        extracted_data = json.loads(response)
        return extracted_data.get("keywords", [])


gpt_service = GPTService()
