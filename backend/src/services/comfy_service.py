# For comfyui
from comfy_script.runtime import *

load("http://127.0.0.1:8188/")
from comfy_script.runtime.nodes import *
from comfy_script.runtime import util


def comfy_api(prompt, lora, seed, batch_size, style_strength, width, height):
    with Workflow():
        model, clip, vae = CheckpointLoaderSimple(
            "juggernautXL_v8Rundiffusion.safetensors"
        )
        model, clip = LoraLoader(model, clip, lora, style_strength, 1)
        conditioning = CLIPTextEncode(prompt, clip)
        conditioning2 = CLIPTextEncode("text, watermark", clip)
        latent = EmptyLatentImage(width, height, batch_size)
        latent = KSampler(
            model,
            seed,
            20,
            8,
            "euler",
            "normal",
            conditioning,
            conditioning2,
            latent,
            1,
        )
        image = VAEDecode(latent, vae)
        return SaveImage(image, "ComfyUI")


def get_img_str(output, style, seed, batch_size, style_strength, width, height):
    img = comfy_api(output, style, seed, batch_size, style_strength, width, height)
    
    # Handle both single images and batches
    if isinstance(img, list):
        # If it's a batch, convert each image to base64
        return [util.get_str(single_img) for single_img in img]
    else:
        # If it's a single image, convert it to base64
        return [util.get_str(img)]
