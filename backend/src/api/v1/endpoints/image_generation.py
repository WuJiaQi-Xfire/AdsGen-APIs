import json
import logging
from fastapi import APIRouter, HTTPException, Form
from src.schemas.image_generation import ImageGenerationResponse
from src.services.image_service import image_service

# Setup logging
logger = logging.getLogger(__name__)

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

    Example:
    - **prompts**: JSON array string containing prompt objects
      ```json
      [{"name": "test_prompt", "content": "A beautiful landscape with {art_style_list}", "selected": true}]
      ```

    - **style_settings**: JSON array string containing style setting objects
      ```json
      [{"id": "anime.safetensors", "styleStrength": 0.8, "batchSize": 1, "styleType": "lora"}]
      ```

    - **keywords**: JSON array string or plain string
      ```json
      ["fantasy", "colorful", "detailed"]
      ```
      or
      ```
      fantasy, colorful, detailed
      ```

    - **stack_loras**: Boolean value
      ```
      true
      ```
      or
      ```
      false
      ```
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
        # 创建详细的错误信息
        error_detail = {
            "error_code": "IMAGE_GENERATION_API_ERROR",
            "message": str(e),
            "request_data": {
                "prompts_count": len(json.loads(prompts)) if prompts else 0,
                "style_settings_count": len(json.loads(style_settings)) if style_settings else 0,
                "keywords": keywords,
                "stack_loras": stack_loras
            }
        }
        
        # 记录详细的错误信息到日志
        logger.error(f"Error in generate_image API: {json.dumps(error_detail, indent=2)}")
        
        # 打印简单的错误信息到控制台
        print(f"Error in generate_image: {str(e)}")
        
        # 抛出简单的错误信息给前端
        raise HTTPException(status_code=500, detail=str(e)) from e
