from fastapi import APIRouter, HTTPException, Form
from src.schemas.image_generation import ImageGenerationResponse
from src.services.image_service import image_service

router = APIRouter()


@router.post(
    "/generate-image/",
    response_model=ImageGenerationResponse,
    summary="Generate Images with Different Styles",
)
async def generate_image(
    prompts: str = Form(...),
    style_settings: str = Form(...),
    keywords: str = Form(...),
    stack_loras: bool = Form(...),
):
    """
    Generate images with different styles using ComfyUI API.
    """
    try:
        generated_images = await image_service.generate_images(
            prompts=prompts,
            style_settings=style_settings,
            keywords=keywords,
            stack_loras=stack_loras,
        )

        return ImageGenerationResponse(images=generated_images)

    except Exception as e:
        print(f"Error in generate_image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e
