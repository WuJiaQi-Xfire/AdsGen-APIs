# For organising different api calls
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List
import pandas as pd
import base64
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import os
import random
import asyncio
from ..services import gpt_service, sd_service, file_service

router = APIRouter()

#For image uploads:
@router.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(BytesIO(contents))
        #Could be one of these formats: 'PNG', 'JPEG', 'WEBP', or 'GIF'
        format = image.format 
        buffered = BytesIO()
        image.save(buffered, format=format)
        img_encoded = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return img_encoded
    except UnidentifiedImageError:
        raise HTTPException(
            status_code=400,
            detail=f"Uploaded file '{file.filename}' is not a valid image or is corrupted."
        )
    except Exception as e:
        error_message = (
            f"Image processing error: '{file.filename}': {str(e)}"
        )
        raise HTTPException(status_code=500, detail=error_message)

@router.post("/upload-text-file/")
async def upload_text_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        text_content = contents.decode("utf-8") 
        return text_content
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail=f"Uploaded file '{file.filename}' is not a valid UTF-8 text file."
        )
    except Exception as e:
        error_message = (
            f"An error occurred while processing the text file '{file.filename}': {str(e)}"
        )
        raise HTTPException(status_code=500, detail=error_message)
    
#Not sure if we are allowing csv uploads as prompt files since current prompt is saved as txt...   
@router.post("/upload-csv/")
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(contents)
        # Process the file and extract categories
        if "categories" in df.columns:
            categories = df["categories"].tolist()
            return {"categories": categories}
        else:
            raise HTTPException(status_code=400, detail="File does not contain 'categories' column.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Placeholder for now
@router.get("/generate-prompts/")
async def generate_prompts(categories: List[str], project_style: str):
    try:
        prompts = []
        for category in categories:
            prompt_template = file_service.load_prompt_template(project_style)
            prompt = gpt_service.construct_llm_prompt(prompt_template, category)
            response = await gpt_service.invoke_llm_async(prompt)
            prompts.append(response)
        return {"prompts": prompts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-images/")
async def generate_images(prompt: str, num_images: int = Form(...)):
    try:
        images = []
        for _ in range(num_images):
            seed = random.randint(0, 4294967295)
            image, _ = sd_service.call_sd_api(prompt, seed)
            image_path = file_service.save_image_locally(image)
            images.append(image_path)
        return {"images": images}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))