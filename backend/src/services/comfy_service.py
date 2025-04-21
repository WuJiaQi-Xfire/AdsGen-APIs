"""Module for comfyui api calls"""

import random
import os
from src.services.file_service import file_service
from comfy_script.runtime import *

comfy_server_url = os.getenv("COMFY_SERVER_URL", "http://127.0.0.1:8188/")
load(comfy_server_url)
from comfy_script.runtime.nodes import *


def comfy_call_single_lora(prompt_name, prompt, lora, batch_size, style_strength):
    """Function to call single lora"""
    for i in range(batch_size):
        single_lora(prompt_name, prompt, lora, style_strength)


def single_lora(prompt_name, prompt, lora, style_strength):
    clean_prompt_name = prompt_name.replace(".txt", "")
    clean_lora_name = lora.replace(".safetensors", "")

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
        filename = f"{clean_prompt_name}_{clean_lora_name}_{n}"
        _ = SaveImageKJ(image, filename, file_service.file_path, ".txt", "")


def comfy_call_stacked_lora(prompt_name, prompt, lora_list, batch_size):
    """Function to call stacked loras"""
    for i in range(batch_size):
        stacked_lora(prompt_name, prompt, lora_list)


def stacked_lora(prompt_name, prompt, lora_list):
    clean_prompt_name = prompt_name.replace(".txt", "")
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
        _ = SaveImageKJ(image, filename, file_service.file_path, ".txt", "")


def comfy_call_single_art(prompt_name, prompt, art, batch_size):
    """Function to call single art"""
    for i in range(batch_size):
        single_art(prompt_name, prompt, art)


def single_art(prompt_name, prompt, art):
    clean_prompt_name = prompt_name.replace(".txt", "")
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
        _ = SaveImageKJ(image, filename, file_service.file_path, ".txt", "")


def comfy_call_stacked_art(prompt_name, prompt, batch_size):
    """Function to call stacked arts"""
    for i in range(batch_size):
        stacked_art(prompt_name, prompt)


def stacked_art(prompt_name, prompt):
    clean_prompt_name = prompt_name.replace(".txt", "")
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
        _ = SaveImageKJ(image, filename, file_service.file_path, ".txt", "")
