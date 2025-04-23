"""Module for image processing function"""

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
            output = self.gpt_service.generate_with_prompt(prompt)
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
                output = self.gpt_service.generate_with_prompt(prompt)
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
            output = self.gpt_service.generate_with_prompt(prompt)
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
                output = self.gpt_service.generate_with_prompt(prompt)
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
    ) -> list:
        """Generate images based on prompts and styles, return list of {filename, data}."""

        prompt_list = json.loads(prompts)
        style_settings_list = json.loads(style_settings)

        lora_list = [l for l in style_settings_list if l["styleType"] == "lora"]
        art_list = [l for l in style_settings_list if l["styleType"] == "art"]

        results = []
        for prompt in prompt_list:
            prompt_content = prompt["content"]
            prompt_name = prompt["name"]

            if stack_loras:
                if lora_list:
                    gpt_prompt = self.gpt_service.generate_with_prompt(prompt_content)
                    gpt_prompt += keywords
                    images = comfy_service.comfy_call_stacked_lora(
                        prompt_name,
                        gpt_prompt,
                        lora_list,
                        batch_size=lora_list[0]["batchSize"],
                    )
                    results.extend(images)
                if art_list:
                    gpt_prompt = self.gpt_service.generate_with_prompt(prompt_content)
                    gpt_prompt += keywords
                    images = comfy_service.comfy_call_stacked_art(
                        prompt_name, gpt_prompt, batch_size=art_list[0]["batchSize"]
                    )
                    results.extend(images)
            else:
                for l in lora_list:
                    gpt_prompt = self.gpt_service.generate_with_prompt(prompt_content)
                    gpt_prompt += keywords
                    images = comfy_service.comfy_call_single_lora(
                        prompt_name,
                        gpt_prompt,
                        l["id"],
                        batch_size=l["batchSize"],
                        style_strength=l["styleStrength"],
                    )
                    results.extend(images)
                for a in art_list:
                    gpt_prompt = self.gpt_service.generate_with_prompt(prompt_content)
                    gpt_prompt += keywords
                    images = comfy_service.comfy_call_single_art(
                        prompt_name, gpt_prompt, a["id"], batch_size=a["batchSize"]
                    )
                    results.extend(images)
        return results


image_service = ImageService()
