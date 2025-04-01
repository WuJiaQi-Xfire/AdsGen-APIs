"""Module for routing different endpoints"""

import base64
import json
import random
from typing import Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
import requests
from ..services import gpt_service, file_service, comfy_service

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
        response = requests.get("http://127.0.0.1:8188/models/loras")
        loras = response.json()
        lora_styles = [{"id": lora, "name": lora} for lora in loras]
        if response.status_code != 200:
            raise ConnectionError("Could not connect to ComfyUI server")

        art_styles = file_service.read_art_file()
        return {"loraStyles": lora_styles, "artStyles": art_styles}
    except Exception as e:
        print(f"Error fetching styles: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/generate-image/")
async def generate_image(
    prompts: str = Form(...),
    style_settings: str = Form(...),
    keywords: str = Form(...),
):
    """Function to generate images with comfyui api"""
    try:
        prompt_list = json.loads(prompts)
        style_settings_list = json.loads(style_settings)
        print("All settings: ", style_settings_list)
        images = []
        seeds = []

        for prompt in prompt_list:
            prompt_content = prompt["content"]
            prompt_content = prompt_content.replace("{Keywords}", keywords)

            for style_setting in style_settings_list:
                style_name = style_setting["name"]
                style_strength = float(style_setting["styleStrength"])
                batch_size = int(style_setting["batchSize"])
                width = int(style_setting["width"])
                height = int(style_setting["height"])
                current_prompt = prompt_content.replace("{art_style_list}", style_name)
                output = gpt_service.create_prompt(current_prompt)
                seed = random.randint(0, 4294967295)
                # img_str = comfy_service.get_img_str(
                #    output, style_name, seed, batch_size, style_strength, width, height
                # )
                img_str = ""
                if img_str:
                    image = img_str
                else:
                    raise ValueError(
                        f"ComfyUI did not return expected outputs for style: {style_name}"
                    )
                images.append(f"data:image/png;base64,{image}")
                seeds.append(seed)

        return {"images": images, "seeds": seeds}
    except Exception as e:
        print(f"Error in endpoints.py: generate_image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e
