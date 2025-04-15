"""
Endpoints for prompt and keywords generation route
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from src.services.gpt_service import gpt_service
from src.utils.image_utils import process_image
from src.schemas.generation import PromptGenerationResponse, KeywordGenerationResponse

router = APIRouter()
router.description = (
    "Generation API, " "providing functions for generating prompts and keywords"
)


@router.post(
    "/prompt/",
    response_model=PromptGenerationResponse,
    summary="Generate Prompt from Description and Optional reference Image",
)
async def generate_prompt(
    description: str = Form(...),
    image: Optional[UploadFile] = File(None),
    image_url: Optional[str] = Form(None),
):
    """
    Generate a prompt based on description and optional image input.
    """
    try:
        image_base64 = await process_image(image) if image else None
        output = gpt_service.create_prompt(description, image_base64, image_url)
        return PromptGenerationResponse(generated_prompt=output)
    except Exception as e:
        print(f"Error in generate_prompt: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post(
    "/keywords/",
    response_model=KeywordGenerationResponse,
    summary="Extract Keywords from Image",
)
async def generate_keywords(
    image: Optional[UploadFile] = File(None),
    image_url: Optional[str] = Form(None),
):
    """
    Extract keywords from provided image.
    """
    try:
        image_base64 = await process_image(image) if image else None
        keywords = gpt_service.extract_keywords(image_base64, image_url)
        return KeywordGenerationResponse(keywords=keywords)

    except Exception as e:
        print(f"Error in extract_keywords: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e
