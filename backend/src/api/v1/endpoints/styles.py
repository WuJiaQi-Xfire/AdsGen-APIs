"""
Endpoint for getting styles
"""

from fastapi import APIRouter, HTTPException
import requests
import os
from dotenv import load_dotenv
from src.services.file_service import file_service


load_dotenv(override=False)
LORA_URL = os.getenv("LORA_URL")

router = APIRouter()
router.description = (
    "Retrive styles API, "
    "providing functions for retrieving lora styles from Comfyui and art styles locally"
)


@router.get("/")
async def get_styles():
    """Method to get Lora and Art styles."""
    try:
        response = requests.get(LORA_URL)
        loras = response.json()
        lora_styles = [
            {"id": lora, "name": lora, "styleType": "lora"} for lora in loras
        ]
        if response.status_code != 200:
            raise ConnectionError("Could not connect to ComfyUI server")

        art_styles = file_service.read_art_file()
        return {"loraStyles": lora_styles, "artStyles": art_styles}
    except Exception as e:
        print(f"Error fetching styles: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e
