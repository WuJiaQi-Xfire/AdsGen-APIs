"""Module for calling sd api"""

import os
import base64
from io import BytesIO
import random
import requests
from dotenv import load_dotenv
from PIL import Image

# Load env variables
env_path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(dotenv_path=env_path)

sd_base_url: str = os.getenv("SD_BASE_URL")

seed = random.randint(0, 4294967295)

def call_sd_api(
    prompt,
    width,
    height,
    batch_size
):
    url=sd_base_url
    payload={
        "batch size": batch_size,
        "cfg_scale": 1,
        "distilled_cfg_scale": 3.5,
        "height": height,
        "prompt": prompt,
        "negative_prompt": "Text, Captions, Watermark, Signature, Cropped",
        "sampler_name": "Euler",
        "scheduler": "Simple",
        "seed": seed,
        "steps": 20,
        "width": width,
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        r = response.json()
        image_data = base64.b64decode(r["images"][0])
        image = Image.open(BytesIO(image_data))
        return image, seed
    else:
        raise Exception(f"Failed to get response from SD API: {response.text}")
