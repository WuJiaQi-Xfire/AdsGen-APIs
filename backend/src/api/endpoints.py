"""Module for routing different endpoints"""

import json
from typing import Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form

import requests

from src.services import gpt_service, file_service, comfy_service
from src.utils.image_utils import process_image
from src.services.image_service import calculate_expected_images, wait_for_images


router = APIRouter()

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

        file_service.clear_image_folders()

        for prompt in prompt_list:
            prompt_content = prompt["content"]
            prompt_name = prompt["name"]
            if lora_list:
                if stack_loras:
                    style_str = " ".join(
                        [f"{l["id"]}:{l["styleStrength"]}" for l in lora_list]
                    )
                    prompt = prompt_content.replace("{art_style_list}", style_str)
                    messages = gpt_service.create_message(prompt)
                    output = gpt_service.make_api_call(messages)
                    output += keywords
                    first_style = lora_list[0]
                    batch_size = int(first_style["batchSize"])
                    # ratio = first_style["aspectRatio"]
                    comfy_service.comfy_call_stacked_lora(
                        prompt_name, output, lora_list, batch_size
                    )
                else:
                    for l in lora_list:
                        prompt = prompt_content.replace(
                            "{art_style_list}", f"{l["id"]}:{l["styleStrength"]}"
                        )
                        messages = gpt_service.create_message(prompt)
                        output = gpt_service.make_api_call(messages)
                        output += keywords
                        print("prompt name: ", prompt_name, ": ", output)
                        batch_size = int(l["batchSize"])
                        # ratio = l["aspectRatio"]
                        style_strength = float(l["styleStrength"])
                        comfy_service.comfy_call_single_lora(
                            prompt_name,
                            output,
                            l["id"],
                            batch_size,
                            style_strength,
                        )
            if art_list:
                if stack_loras:
                    style_str = " ".join(
                        [f"{a["id"]}:{a["styleStrength"]}" for a in art_list]
                    )
                    prompt = prompt_content.replace("{art_style_list}", style_str)
                    messages = gpt_service.create_message(prompt)
                    output = gpt_service.make_api_call(messages)
                    output += keywords
                    first_style = art_list[0]
                    batch_size = int(first_style["batchSize"])
                    # ratio = first_style["aspectRatio"]
                    comfy_service.comfy_call_stacked_art(
                        prompt_name,
                        output,
                        batch_size,
                    )
                else:
                    for a in art_list:
                        prompt = prompt_content.replace(
                            "{art_style_list}", f"{a["id"]}:{a["styleStrength"]}"
                        )
                        messages = gpt_service.create_message(prompt)
                        output = gpt_service.make_api_call(messages)
                        output += keywords
                        batch_size = int(a["batchSize"])
                        # ratio = a["aspectRatio"]
                        comfy_service.comfy_call_single_art(
                            prompt_name,
                            output,
                            a["id"],
                            batch_size,
                        )

        expected_images = calculate_expected_images(
            prompt_list, lora_list, art_list, stack_loras
        )
        print(f"Expecting {expected_images} images to be generated")
        success = wait_for_images(expected_images)
        generated_images = file_service.get_generated_images()
        return {"images": generated_images}

    except Exception as e:
        print(f"Error in endpoints.py: generate_image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e
