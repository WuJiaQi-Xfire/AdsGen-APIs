"""
Endpoint for getting styles
"""

from fastapi import APIRouter, HTTPException
import requests
import os
import json
import logging
from dotenv import load_dotenv
from src.services.file_service import file_service
from src.services.comfy_service import check_comfy_available, COMFY_URL


# Setup logging
logger = logging.getLogger(__name__)

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
        lora_styles = []
        
        # Check if ComfyUI is available
        if check_comfy_available() and LORA_URL:
            try:
                response = requests.get(LORA_URL, timeout=5)
                if response.status_code == 200:
                    loras = response.json()
                    lora_styles = [
                        {"id": lora, "name": lora, "styleType": "lora"} for lora in loras
                    ]
                else:
                    error_detail = {
                        "error_code": "LORA_API_ERROR",
                        "message": f"ComfyUI returned status code {response.status_code}",
                        "service_status": {
                            "comfy_url": COMFY_URL,
                            "lora_url": LORA_URL,
                            "status_code": response.status_code
                        }
                    }
                    logger.warning(f"Error fetching lora styles: {json.dumps(error_detail, indent=2)}")
            except Exception as e:
                error_detail = {
                    "error_code": "LORA_API_EXCEPTION",
                    "message": f"Error fetching lora styles: {str(e)}",
                    "service_status": {
                        "comfy_url": COMFY_URL,
                        "lora_url": LORA_URL
                    }
                }
                logger.warning(f"Exception fetching lora styles: {json.dumps(error_detail, indent=2)}")
        else:
            error_detail = {
                "error_code": "COMFY_UNAVAILABLE",
                "message": "ComfyUI is not available, returning empty lora styles",
                "service_status": {
                    "comfy_url": COMFY_URL,
                    "lora_url": LORA_URL,
                    "comfy_available": check_comfy_available()
                }
            }
            logger.warning(f"ComfyUI unavailable for styles: {json.dumps(error_detail, indent=2)}")

        # Art styles are always available as they're stored locally
        art_styles = file_service.read_art_file()
        
        return {"loraStyles": lora_styles, "artStyles": art_styles}
    except Exception as e:
        error_detail = {
            "error_code": "STYLES_API_ERROR",
            "message": f"Error fetching styles: {str(e)}",
            "service_status": {
                "comfy_url": COMFY_URL,
                "lora_url": LORA_URL,
                "comfy_available": check_comfy_available()
            }
        }
        logger.error(f"Error in get_styles API: {json.dumps(error_detail, indent=2)}")
        raise HTTPException(status_code=500, detail=str(e)) from e
