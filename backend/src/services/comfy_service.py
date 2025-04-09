import os
import base64
import random

# For comfyui
from comfy_script.runtime import *

load("http://127.0.0.1:8188/")
from comfy_script.runtime.nodes import *

# Locally for now
file_path = r"C:\Users\GT0730-1\Documents\GitHub\Ads-Gen\Output\base_image"
# preview_path = r"C:\Users\GT0730-1\Documents\GitHub\Ads-Gen\Output\resized_image"


def comfy_call_single_lora(prompt_name, prompt, lora, batch_size, style_strength):
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
        _ = SaveImageKJ(image, filename, file_path, ".txt", "")


def comfy_call_stacked_lora(prompt_name, prompt, lora_list, batch_size):
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
        _ = SaveImageKJ(image, filename, file_path, ".txt", "")


def comfy_call_single_art(prompt_name, prompt, art, batch_size):
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
        _ = SaveImageKJ(image, filename, file_path, ".txt", "")


def comfy_call_stacked_art(prompt_name, prompt, batch_size):
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
        _ = SaveImageKJ(image, filename, file_path, ".txt", "")


def get_generated_images():
    """Load all images from the resized_image folder and convert them to base64 strings."""
    images = []
    try:
        image_files = [f for f in os.listdir(file_path) if f.lower().endswith((".png"))]
        for image_file in image_files:
            new_path = os.path.join(file_path, image_file)
            with open(new_path, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode("utf-8")
                image_obj = {
                    "filename": image_file,
                    "data": f"data:image/png;base64,{img_data}",
                }
                images.append(image_obj)

        return images
    except Exception as e:
        print(f"Error loading generated images: {str(e)}")
        return []
