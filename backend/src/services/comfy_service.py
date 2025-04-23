"""Module for comfyui api calls"""

import random
import os
from dotenv import load_dotenv
from src.utils import file_utils
from comfy_script.runtime import *
import threading

# Global lock to serialize all ComfyUI Workflow calls
comfy_lock = threading.Lock()

load_dotenv()
COMFY_URL = os.getenv("COMFY_URL")

load(COMFY_URL)
from comfy_script.runtime.nodes import *
from comfy_script.runtime import util


def comfy_call_single_lora(prompt_name, prompt, lora, batch_size, style_strength):
    """Function to call single lora"""
    results = []
    for i in range(batch_size):
        filename, img_str = single_lora(prompt_name, prompt, lora, style_strength)
        results.append({"filename": filename, "data": img_str})
    return results


def single_lora(prompt_name, prompt, lora, style_strength):
    prompt_name = file_utils.sanitize_filename(prompt_name)
    clean_prompt_name = prompt_name.replace(".txt", "")
    with comfy_lock:
        with Workflow():
            n = random.randint(0, 18446744073709551615)
            noise = RandomNoise(n)
            model = UNETLoader("flux1-dev-fp8.safetensors", "default")
            clip = DualCLIPLoader(
                "clip_l.safetensors", "t5xxl_fp8_e4m3fn.safetensors", "flux", "default"
            )
            model, clip = LoraLoader(model, clip, lora, style_strength, 1)
            model = ModelSamplingFlux(
                model, 1.1500000000000001, 0.5000000000000001, 1088, 1088
            )
            conditioning = CLIPTextEncode(prompt, clip)
            conditioning = FluxGuidance(conditioning, 3.5)
            guider = BasicGuider(model, conditioning)
            sampler = KSamplerSelect("euler")
            sigmas = BasicScheduler(model, "simple", 30, 1)
            latent = EmptyLatentImage(1088, 1088, 1)
            latent, _ = SamplerCustomAdvanced(noise, guider, sampler, sigmas, latent)
            vae = VAELoader("ae.safetensors")
            image = VAEDecode(latent, vae)
            lora = file_utils.sanitize_filename(lora)
            clean_lora_name = lora.replace(".safetensors", "")
            filename = f"{clean_prompt_name}_{clean_lora_name}_{n}.png"
            image_64 = SaveImage64(image, "ComfyUI")
            img_str = util.get_str(image_64)
            img_str = clean_base64(img_str)
            return filename, img_str


def comfy_call_stacked_lora(prompt_name, prompt, lora_list, batch_size):
    """Function to call stacked loras"""
    results = []
    for i in range(batch_size):
        filename, img_str = stacked_lora(prompt_name, prompt, lora_list)
        results.append({"filename": filename, "data": img_str})
    return results


def stacked_lora(prompt_name, prompt, lora_list):
    prompt_name = file_utils.sanitize_filename(prompt_name)
    clean_prompt_name = prompt_name.replace(".txt", "")
    with comfy_lock:
        with Workflow():
            n = random.randint(0, 18446744073709551615)
            noise = RandomNoise(n)
            model = UNETLoader("flux1-dev-fp8.safetensors", "default")
            clip = DualCLIPLoader(
                "clip_l.safetensors", "t5xxl_fp8_e4m3fn.safetensors", "flux", "default"
            )
            for l in lora_list:
                model, clip = LoraLoader(model, clip, l["id"], l["styleStrength"], 1)
            model = ModelSamplingFlux(
                model, 1.1500000000000001, 0.5000000000000001, 1088, 1088
            )
            conditioning = CLIPTextEncode(prompt, clip)
            conditioning = FluxGuidance(conditioning, 3.5)
            guider = BasicGuider(model, conditioning)
            sampler = KSamplerSelect("euler")
            sigmas = BasicScheduler(model, "simple", 30, 1)
            latent = EmptyLatentImage(1080, 1080, 1)
            latent, _ = SamplerCustomAdvanced(noise, guider, sampler, sigmas, latent)
            vae = VAELoader("ae.safetensors")
            image = VAEDecode(latent, vae)
            filename = f"{clean_prompt_name}_stackedLora_{n}"
            image_64 = SaveImage64(image, "ComfyUI")
            img_str = util.get_str(image_64)
            img_str = clean_base64(img_str)
            return filename, img_str


def comfy_call_single_art(prompt_name, prompt, art, batch_size):
    """Function to call single art"""
    results = []
    for i in range(batch_size):
        filename, img_str = single_art(prompt_name, prompt, art)
        results.append({"filename": filename, "data": img_str})
    return results


def single_art(prompt_name, prompt, art):
    prompt_name = file_utils.sanitize_filename(prompt_name)
    clean_prompt_name = prompt_name.replace(".txt", "")
    with comfy_lock:
        with Workflow():
            n = random.randint(0, 18446744073709551615)
            noise = RandomNoise(n)
            model = UNETLoader("flux1-dev-fp8.safetensors", "default")
            model = ModelSamplingFlux(
                model, 1.1500000000000001, 0.5000000000000001, 1088, 1088
            )
            clip = DualCLIPLoader(
                "clip_l.safetensors", "t5xxl_fp8_e4m3fn.safetensors", "flux", "default"
            )
            conditioning = CLIPTextEncode(prompt, clip)
            conditioning = FluxGuidance(conditioning, 3.5)
            guider = BasicGuider(model, conditioning)
            sampler = KSamplerSelect("euler")
            sigmas = BasicScheduler(model, "simple", 30, 1)
            latent = EmptyLatentImage(1080, 1080, 1)
            latent, _ = SamplerCustomAdvanced(noise, guider, sampler, sigmas, latent)
            vae = VAELoader("ae.safetensors")
            image = VAEDecode(latent, vae)
            filename = f"{clean_prompt_name}_{art}_{n}"
            image_64 = SaveImage64(image, "ComfyUI")
            img_str = util.get_str(image_64)
            img_str = clean_base64(img_str)
            return filename, img_str


def comfy_call_stacked_art(prompt_name, prompt, batch_size):
    """Function to call stacked arts"""
    results = []
    for i in range(batch_size):
        filename, img_str = stacked_art(prompt_name, prompt)
        results.append({"filename": filename, "data": img_str})
    return results


def stacked_art(prompt_name, prompt):
    prompt_name = file_utils.sanitize_filename(prompt_name)
    clean_prompt_name = prompt_name.replace(".txt", "")
    with comfy_lock:
        with Workflow():
            n = random.randint(0, 18446744073709551615)
            noise = RandomNoise(n)
            model = UNETLoader("flux1-dev-fp8.safetensors", "default")
            model = ModelSamplingFlux(
                model, 1.1500000000000001, 0.5000000000000001, 1088, 1088
            )
            clip = DualCLIPLoader(
                "clip_l.safetensors", "t5xxl_fp8_e4m3fn.safetensors", "flux", "default"
            )
            conditioning = CLIPTextEncode(prompt, clip)
            conditioning = FluxGuidance(conditioning, 3.5)
            guider = BasicGuider(model, conditioning)
            sampler = KSamplerSelect("euler")
            sigmas = BasicScheduler(model, "simple", 30, 1)
            latent = EmptyLatentImage(1080, 1080, 1)
            latent, _ = SamplerCustomAdvanced(noise, guider, sampler, sigmas, latent)
            vae = VAELoader("ae.safetensors")
            image = VAEDecode(latent, vae)
            filename = f"{clean_prompt_name}_stacked_art_{n}"
            image_64 = SaveImage64(image, "ComfyUI")
            img_str = util.get_str(image_64)
            img_str = clean_base64(img_str)
            return filename, img_str


def clean_base64(img_str):
    # If it's a list, join or take the first element
    if isinstance(img_str, list):
        # If list of strings, join or take first (most common: single string in list)
        img_str = img_str[0] if len(img_str) == 1 else "".join(img_str)
    # If it's a string that looks like a list, strip brackets and quotes
    if isinstance(img_str, str):
        img_str = img_str.strip()
        if img_str.startswith("['") and img_str.endswith("']"):
            img_str = img_str[2:-2]
        elif img_str.startswith("[") and img_str.endswith("]"):
            img_str = img_str[1:-1]
        # Remove any stray quotes
        img_str = img_str.strip("'\"")
    return img_str
