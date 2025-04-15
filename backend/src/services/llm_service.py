"""Module for LLM service"""

from typing import Optional, Dict, Any, List
from src.utils.image_utils import validate_image_url


class LLMService:
    def __init__(self):
        self.default_params = {
            "temperature": 0.8,
            "top_p": 0.6,
            "max_tokens": 4000,
        }

    def create_message(
        self,
        content: str,
        image_url: Optional[str] = None,
        image_base64: Optional[str] = None,
        system_prompt: str = "You are a creative assistant.",
    ) -> List[Dict[str, Any]]:
        """
        Create messages for LLM requests with optional image content.
        """
        messages = [
            {"role": "system", "content": system_prompt},
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

    def prepare_request_data(
        self,
        messages: List[Dict[str, Any]],
        response_format: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Prepare request data with optional response format and custom parameters.
        """
        data = {**self.default_params, "messages": messages, **kwargs}

        if response_format:
            data["response_format"] = response_format

        return data


llm_service = LLMService()
