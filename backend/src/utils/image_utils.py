"""Image utility functions"""

import requests


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
