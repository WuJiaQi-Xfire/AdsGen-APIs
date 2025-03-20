# For organising different api calls
import base64
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Optional
from ..services import gpt_service, sd_service

router = APIRouter()


# For testing
@router.get("/backend")
async def read_root():
    return {"message": "Connected to frontend"}


@router.post("/generate-prompt/")
async def generate_prompt(
    description: str = Form(...),
    image: Optional[UploadFile] = File(None),
    image_url: Optional[str] = Form(None),
):
    try:
        image_base64 = None
        if image:
            contents = await image.read()
            image_base64 = base64.b64encode(contents).decode("utf-8")
        output = gpt_service.create_prompt(description, image_base64, image_url)
        print("Output: ", output)
        return {"generated_prompt": output}
    except Exception as e:
        print(f"Error in endpoints.py: generate_prompt: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract-keywords/")
async def extract_keywords(image: UploadFile = File(None), image_url: str = Form(None)):
    try:
        image_base64 = None
        if image:
            contents = await image.read()
            image_base64 = base64.b64encode(contents).decode("utf-8")
        keywords = gpt_service.extract_keywords(image_base64, image_url)
        return {"keywords": keywords}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
