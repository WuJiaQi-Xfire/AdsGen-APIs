"""Module for image processing function"""

import time
import asyncio
import json
from io import BytesIO
import base64
from typing import List, Dict, Any
from src.services.gpt_service import gpt_service
from src.services.file_service import file_service
from src.services import comfy_service
from PIL import Image


class ImageService:
    """Module for functions related to image generation"""

    def __init__(self):
        self.gpt_service = gpt_service
        self.file_service = file_service

    def layer_template_over_base(
        self, base_image_path: str, template_png_path: str
    ) -> str:
        """
        Composite a PNG template over a base PNG image and return the result as a base64 PNG string.
        """

        # Open both images as RGBA
        base_img = Image.open(base_image_path).convert("RGBA")
        template_img = (
            Image.open(template_png_path).convert("RGBA").resize(base_img.size)
        )

        # Composite the template over the base image
        result_img = Image.alpha_composite(base_img, template_img)

        # Encode as base64 PNG
        buffer = BytesIO()
        result_img.save(buffer, format="PNG")
        img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{img_b64}"

    def process_lora_styles(
        self,
        prompt_content: str,
        prompt_name: str,
        lora_list: List[Dict[str, Any]],
        keywords: str,
        stack_loras: bool,
    ):
        """Process lora styles and generate images."""
        if stack_loras:
            style_str = " ".join([f"{l['id']}:{l['styleStrength']}" for l in lora_list])
            prompt = prompt_content.replace("{art_style_list}", style_str)
            output = self.gpt_service.create_prompt(prompt)
            output += keywords
            first_style = lora_list[0]
            batch_size = int(first_style["batchSize"])

            comfy_service.comfy_call_stacked_lora(
                prompt_name, output, lora_list, batch_size
            )
        else:
            for l in lora_list:
                prompt = prompt_content.replace(
                    "{art_style_list}", f"{l['id']}:{l['styleStrength']}"
                )
                output = self.gpt_service.create_prompt(prompt)
                output += keywords
                batch_size = int(l["batchSize"])
                style_strength = float(l["styleStrength"])

                comfy_service.comfy_call_single_lora(
                    prompt_name,
                    output,
                    l["id"],
                    batch_size,
                    style_strength,
                )

    def process_art_styles(
        self,
        prompt_content: str,
        prompt_name: str,
        art_list: List[Dict[str, Any]],
        keywords: str,
        stack_loras: bool,
    ):
        """Process art styles and generate images."""
        if stack_loras:
            style_str = " ".join([f"{a['id']}:{a['styleStrength']}" for a in art_list])
            prompt = prompt_content.replace("{art_style_list}", style_str)
            output = self.gpt_service.create_prompt(prompt)
            output += keywords
            first_style = art_list[0]
            batch_size = int(first_style["batchSize"])

            comfy_service.comfy_call_stacked_art(
                prompt_name,
                output,
                batch_size,
            )
        else:
            for a in art_list:
                prompt = prompt_content.replace(
                    "{art_style_list}", f"{a['id']}:{a['styleStrength']}"
                )
                output = self.gpt_service.create_prompt(prompt)
                output += keywords
                batch_size = int(a["batchSize"])

                comfy_service.comfy_call_single_art(
                    prompt_name,
                    output,
                    a["id"],
                    batch_size,
                )

    async def generate_images(
        self, prompts: str, style_settings: str, keywords: str, stack_loras: bool
    ) -> List[Dict[str, str]]:
        """Generate images based on prompts and styles."""
        prompt_list = json.loads(prompts)
        style_settings_list = json.loads(style_settings)

        lora_list = [l for l in style_settings_list if l["styleType"] == "lora"]
        art_list = [l for l in style_settings_list if l["styleType"] == "art"]

        self.file_service.clear_image_folders()

        # Process prompts synchronously
        for prompt in prompt_list:
            prompt_content = prompt["content"]
            prompt_name = prompt["name"]

            if lora_list:
                self.process_lora_styles(
                    prompt_content, prompt_name, lora_list, keywords, stack_loras
                )

            if art_list:
                self.process_art_styles(
                    prompt_content, prompt_name, art_list, keywords, stack_loras
                )

        expected_images = self.calculate_expected_images(
            prompt_list, lora_list, art_list, stack_loras
        )
        print(f"Expecting {expected_images} images to be generated")

        await self.wait_for_images(expected_images)

        return self.file_service.get_generated_images()

    def calculate_expected_images(self, prompt_list, lora_list, art_list, stack_loras):
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

    async def wait_for_images(
        self, expected_count: int, check_interval: int = 110
    ) -> bool:
        """Asynchronously wait for images to be generated."""
        start_time = time.time()
        last_count = 0
        last_check_time = start_time

        print(f"Waiting for {expected_count} images to be generated...")

        while True:
            try:
                image_files = self.file_service.get_generated_images()
                current_count = len(image_files)
                current_time = time.time()
                elapsed_minutes = (current_time - start_time) / 60

                if (
                    current_count > last_count
                    or (current_time - last_check_time) >= check_interval
                ):
                    print(
                        f"Progress after {elapsed_minutes:.1f} minutes: "
                        f"{current_count}/{expected_count} images generated"
                    )
                    last_count = current_count
                    last_check_time = current_time

                if current_count >= expected_count:
                    total_minutes = (time.time() - start_time) / 60
                    print(
                        f"All {expected_count} images have been generated "
                        f"successfully in {total_minutes:.1f} minutes!"
                    )
                    return True

                await asyncio.sleep(check_interval)

            except Exception as e:
                print(f"Error while waiting for images: {str(e)}")
                raise


image_service = ImageService()
