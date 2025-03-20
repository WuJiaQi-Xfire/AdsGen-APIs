import requests
from PIL import Image
from io import BytesIO
import base64
import os

sd_base_url: str = os.getenv("SD_BASE_URL")


# Placeholder for now
def call_sd_api(prompt: str, seed: int):
    # Call the Stable Diffusion API
    response = requests.post("SD_API_ENDPOINT", json={"prompt": prompt, "seed": seed})
    if response.status_code == 200:
        image_data = base64.b64decode(response.json()["image"])
        image = Image.open(BytesIO(image_data))
        return image, seed
    else:
        raise Exception("Failed to get response from SD API")
