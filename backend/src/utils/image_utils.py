"""Image utility functions"""

from typing import Optional
import base64
import requests
from fastapi import UploadFile



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


async def process_image(image: Optional[UploadFile]) -> Optional[str]:
    """Function to convert image to base64."""
    if image:
        contents = await image.read()
        return base64.b64encode(contents).decode("utf-8")
    return None

