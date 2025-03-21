"""Module for routing different endpoints"""

import base64
from typing import Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from ..services import gpt_service, sd_service, file_service

router = APIRouter()


async def process_image(image: Optional[UploadFile]) -> Optional[str]:
    """Function to convert image to base64."""
    if image:
        contents = await image.read()
        return base64.b64encode(contents).decode("utf-8")
    return None


@router.post("/generate-prompt/")
async def generate_prompt(
    description: str = Form(...),
    image: Optional[UploadFile] = File(None),
    image_url: Optional[str] = Form(None),
):
    """Method to handle prompt generation request"""
    try:
        image_base64 = await process_image(image)
        output = gpt_service.create_prompt(description, image_base64, image_url)
        # For debugging:
        # print("Generated Prompt: ", output)
        return {"generated_prompt": output}
    except Exception as e:
        print(f"Error in endpoints.py: generate_prompt: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/extract-keywords/")
async def extract_keywords(
    image: Optional[UploadFile] = File(None),
    image_url: Optional[str] = Form(None),
):
    """Method to extract keywords from image"""
    try:
        image_base64 = await process_image(image)
        keywords = gpt_service.extract_keywords(image_base64, image_url)
        # For debugging:
        # print("Extracted keywords: ", keywords)
        return {"keywords": keywords}
    except Exception as e:
        print(f"Error in endpoints.py: extract_keywords: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/get-styles/")
async def get_styles():
    """Method to get Lora and Art styles."""
    try:
        lora_styles = file_service.read_lora_file()
        art_styles = file_service.read_art_file()
        # For debugging
        # print("loraStyles: ", lora_styles, " artStyles: ", art_styles)
        return {"loraStyles": lora_styles, "artStyles": art_styles}
    except Exception as e:
        print(f"Error fetching styles: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/generate-image/")
async def generate_image(
    prompts: str = Form(...),
    styles: str = Form(...),
    style_type: str = Form(...),
    style_strength: int = Form(...),
    width: int = Form(...),
    height: int = Form(...),
    batch_size: int = Form(...),
    keywords: str = Form(...),
):
    try:
        # Parse JSON strings into Python objects
        selected_prompts = [PromptFile(**pf) for pf in json.loads(prompts)]
        selected_styles = json.loads(styles)
        keywords_list = json.loads(keywords)

        images = sd_service.generate_images(
            selected_prompts,
            selected_styles,
            style_type,
            style_strength,
            width,
            height,
            batch_size,
            keywords_list,
        )
        return {"images": images}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
