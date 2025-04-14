"""Module for LLM service"""

from src.utils.image_utils import validate_image_url


def create_message(content, image_url=None, image_base64=None):
    """Function to create messages for LLM requests."""
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
