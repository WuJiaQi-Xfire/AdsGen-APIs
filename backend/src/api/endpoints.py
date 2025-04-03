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


@router.post("/generate-image/")
async def generate_image(
    prompts: str = Form(...),
    style_settings: str = Form(...),
    keywords: str = Form(...),
    stack_loras: bool = Form(...),
):
    """Function to generate images with comfyui api"""
    try:
        prompt_list = json.loads(prompts)
        style_settings_list = json.loads(style_settings)
        lora_list = [l for l in style_settings_list if l["styleType"] == "lora"]
        art_list = [l for l in style_settings_list if l["styleType"] == "art"]
        images = []
        seeds = []
        for prompt in prompt_list:
            prompt_content = prompt["content"]
            prompt_content = prompt_content.replace("{Keywords}", keywords)
            if lora_list:
                if stack_loras:
                    style_str = " ".join(
                        [f"{l["id"]}:{l["styleStrength"]}" for l in lora_list]
                    )
                    prompt = prompt_content.replace("{art_style_list}", style_str)
                    seed = random.randint(0, 4294967295)
                    batch_size = int(lora_list[0]["batchSize"])
                    ratio = lora_list[0]["aspectRatio"]
                    print("Stacked style calling comfyui with: ", lora_list)
                    results = comfy_service.stacked_style_str(
                        prompt, lora_list, seed, batch_size, ratio
                    )
                else:
                    for l in lora_list:
                        prompt = prompt_content.replace(
                            "{art_style_list}", f"{l[id]}:{l["styleStrength"]}"
                        )
                        batch_size = int(l["batchSize"])
                        ratio = l["aspectRatio"]
                        seed = random.randint(0, 4294967295)
                        style_strength = float(l["styleStrength"])
                        print("Single style calling comfyui with: ", lora_list)
                        results = comfy_service.single_style_str(
                            prompt,
                            l["id"],
                            seed,
                            batch_size,
                            style_strength,
                            ratio,
                        )
            if art_list:
                if stack_loras:
                    style_str = " ".join(
                        [f"{a["id"]}:{a["styleStrength"]}" for a in art_list]
                    )
                    prompt = prompt_content.replace("{art_style_list}", style_str)
                    seed = random.randint(0, 4294967295)
                    batch_size = int(art_list[0]["batchSize"])
                    ratio = art_list[0]["aspectRatio"]
                    print("Stacked style calling comfyui with: ", art_list)
                    results = comfy_service.stacked_style_str(
                        prompt, "", seed, batch_size, ratio
                    )
                else:
                    for a in art_list:
                        prompt = prompt_content.replace(
                            "{art_style_list}", f"{a[id]}:{a["styleStrength"]}"
                        )
                        batch_size = int(a["batchSize"])
                        ratio = a["aspectRatio"]
                        seed = random.randint(0, 4294967295)
                        print("Single style calling comfyui with: ", art_list)
                        results = comfy_service.single_style_str(
                            prompt, "", seed, batch_size, 1.0, ratio
                        )
                if results:
                    images.append(f"data:image/png;base64,{results}")
                    seeds.append(seed)
                else:
                    raise ValueError(f"ComfyUI did not return any image string")

        return {"images": images, "seeds": seeds}
    except Exception as e:
        print(f"Error in endpoints.py: generate_image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e
