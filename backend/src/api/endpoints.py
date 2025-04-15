"""Module for routing different endpoints"""

import json
from fastapi import APIRouter, HTTPException, Form

from src.services import file_service, comfy_service
from src.services.gpt_service import gpt_service
from src.services.image_service import calculate_expected_images, wait_for_images


router = APIRouter()


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
                    output = gpt_service.create_prompt(prompt)
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
                        output = gpt_service.create_prompt(prompt)
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
                    output = gpt_service.create_prompt(prompt)
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
                        output = gpt_service.create_prompt(prompt)
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
