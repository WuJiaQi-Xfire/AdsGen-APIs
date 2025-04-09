"""Module for routing different endpoints"""

import base64
import json
import time
import os
from typing import Optional, List
from datetime import datetime
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
import requests
from pydantic import BaseModel
from src.services.comfy_service import file_path
from ..services import gpt_service, file_service, comfy_service
from ..database.database import DatabaseManager

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


class PromptModel(BaseModel):
    prompt_name: str
    content: str


class PromptResponse(BaseModel):
    id: int
    prompt_name: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}


def get_db():
    db = DatabaseManager()
    try:
        yield db
    finally:
        del db


@router.post("/prompts/", response_model=dict)
async def create_prompt(prompt: PromptModel, db: DatabaseManager = Depends(get_db)):
    """Create a new prompt in the database"""
    try:
        prompt_id = db.save_prompt(prompt.prompt_name, prompt.content)
        return {"id": prompt_id, "message": "Prompt saved successfully"}
    except Exception as e:
        print(f"Error saving prompt: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/prompts/", response_model=List[PromptResponse])
async def get_prompts(db: DatabaseManager = Depends(get_db)):
    """Get all prompts from the database"""
    try:
        prompts = db.list_prompts()
        return prompts
    except Exception as e:
        print(f"Error getting prompts: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/prompts/{prompt_id}", response_model=PromptResponse)
async def get_prompt(prompt_id: int, db: DatabaseManager = Depends(get_db)):
    """Get a prompt by ID"""
    try:
        prompt = db.get_prompt(prompt_id)
        if not prompt:
            raise HTTPException(status_code=404, detail="Prompt not found")
        return prompt
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting prompt: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/prompts/{prompt_id}")
async def delete_prompt(prompt_id: int, db: DatabaseManager = Depends(get_db)):
    """Delete a prompt by ID"""
    try:
        success = db.delete_prompt(prompt_id)
        if not success:
            raise HTTPException(status_code=404, detail="Prompt not found")
        return {"message": "Prompt deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting prompt: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e


def calculate_expected_images(prompt_list, lora_list, art_list, stack_loras):
    """Calculate the expected number of images to be generated."""
    expected_count = 0
    prompt_count = len(prompt_list)

    if stack_loras:
        # When stacked, generate one image per prompt for each group
        if lora_list:
            # For stacked loras, use the batch size from the first lora
            expected_count += prompt_count * int(lora_list[0].get("batchSize", 1))
        if art_list:
            # For stacked arts, use the batch size from the first art style
            expected_count += prompt_count * int(art_list[0].get("batchSize", 1))
    else:
        # When not stacked, generate images for each style individually
        for l in lora_list:
            expected_count += prompt_count * int(l.get("batchSize", 1))
        for a in art_list:
            expected_count += prompt_count * int(a.get("batchSize", 1))

    return expected_count


def wait_for_images(expected_count, check_interval=110):
    """Wait for the expected number of images to be generated."""
    start_time = time.time()
    last_count = 0
    last_check_time = start_time

    print(f"Waiting for {expected_count} images to be generated...")

    while True:
        try:
            image_files = [
                f for f in os.listdir(file_path) if f.lower().endswith((".png"))
            ]
            current_count = len(image_files)
            current_time = time.time()
            elapsed_minutes = (current_time - start_time) / 60
            if (
                current_count > last_count
                or (current_time - last_check_time) >= check_interval
            ):
                print(
                    f"Progress after {elapsed_minutes:.1f} minutes: {current_count}/{expected_count} images generated"
                )
                last_count = current_count
                last_check_time = current_time

            if current_count >= expected_count:
                total_minutes = (time.time() - start_time) / 60
                print(
                    f"All {expected_count} images have been generated successfully in {total_minutes:.1f} minutes!"
                )
                return True

            time.sleep(check_interval)

        except Exception as e:
            print(f"Error while waiting for images: {str(e)}")
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
        generated_images = comfy_service.get_generated_images()
        return {"images": generated_images}

    except Exception as e:
        print(f"Error in endpoints.py: generate_image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e
