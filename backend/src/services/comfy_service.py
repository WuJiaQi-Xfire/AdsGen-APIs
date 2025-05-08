"""Module for comfyui api calls"""

import random
import os
import json
import logging
from src.utils import file_utils
import threading
import importlib.util

# Global lock to serialize all ComfyUI Workflow calls
comfy_lock = threading.Lock()

# Setup logging
logger = logging.getLogger(__name__)

# Load environment variables
COMFY_URL = os.getenv("COMFY_URL")

# Flag to track if ComfyUI is available
comfy_available = False
# Import comfy_script modules and initialize connection first
try:
    if importlib.util.find_spec("comfy_script") is not None:
        # First import only the load function
        from comfy_script.runtime import load
        
        # Try to initialize ComfyUI connection BEFORE importing nodes
        try:
            if COMFY_URL:
                load(COMFY_URL)
                comfy_available = True
                logger.info(f"Successfully connected to ComfyUI at {COMFY_URL}")
                
                # Only import nodes AFTER successful connection
                from comfy_script.runtime import Workflow
                from comfy_script.runtime.nodes import (
                    RandomNoise, UNETLoader, DualCLIPLoader, LoraLoader, 
                    ModelSamplingFlux, CLIPTextEncode, FluxGuidance, BasicGuider, 
                    KSamplerSelect, BasicScheduler, EmptyLatentImage, 
                    SamplerCustomAdvanced, VAELoader, VAEDecode, SaveImage64, SaveImage
                )
                from comfy_script.runtime import util
            else:
                logger.warning("COMFY_URL not set in environment variables")
        except Exception as e:
            error_detail = {
                "error_code": "COMFY_CONNECTION_FAILED",
                "message": f"Failed to connect to ComfyUI: {str(e)}",
                "service_status": {
                    "comfy_url": COMFY_URL
                }
            }
            logger.warning(f"ComfyUI connection failed: {json.dumps(error_detail, indent=2)}")
    else:
        error_detail = {
            "error_code": "COMFY_MODULE_NOT_FOUND",
            "message": "comfy_script module not found",
            "service_status": {
                "comfy_url": COMFY_URL
            }
        }
        logger.warning(f"ComfyUI module issue: {json.dumps(error_detail, indent=2)}")
except ImportError as e:
    error_detail = {
        "error_code": "COMFY_IMPORT_ERROR",
        "message": f"Failed to import comfy_script: {str(e)}",
        "service_status": {
            "comfy_url": COMFY_URL
        }
    }
    logger.warning(f"ComfyUI import error: {json.dumps(error_detail, indent=2)}")

def check_comfy_available():
    """Check if ComfyUI is available and try to reconnect if not"""
    global comfy_available
    
    if not comfy_available and COMFY_URL:
        try:
            # Try to reconnect to ComfyUI
            load(COMFY_URL)
            comfy_available = True
            logger.info(f"Successfully reconnected to ComfyUI at {COMFY_URL}")
        except Exception as e:
            error_detail = {
                "error_code": "COMFY_RECONNECTION_FAILED",
                "message": f"Failed to reconnect to ComfyUI: {str(e)}",
                "service_status": {
                    "comfy_url": COMFY_URL
                }
            }
            logger.warning(f"ComfyUI reconnection failed: {json.dumps(error_detail, indent=2)}")
    
    return comfy_available

def comfy_call_single_lora(prompt_name, prompt, lora, batch_size, style_strength):
    """Function to call single lora"""
    if not check_comfy_available():
        error_detail = {
            "error_code": "COMFY_UNAVAILABLE",
            "message": "ComfyUI is not available",
            "request_data": {
                "prompt_name": prompt_name,
                "prompt_length": len(prompt) if prompt else 0,
                "lora": lora,
                "batch_size": batch_size,
                "style_strength": style_strength
            },
            "service_status": {
                "comfy_url": COMFY_URL,
                "comfy_available": comfy_available
            }
        }
        logger.error(f"ComfyUI is not available for single lora call: {json.dumps(error_detail, indent=2)}")
        raise RuntimeError("ComfyUI is not available")
        
    results = []
    for i in range(batch_size):
        filename, img_str = single_lora(prompt_name, prompt, lora, style_strength)
        results.append({"filename": filename, "data": img_str})
    return results


def single_lora(prompt_name, prompt, lora, style_strength):
    if not check_comfy_available():
        error_detail = {
            "error_code": "COMFY_UNAVAILABLE",
            "message": "ComfyUI is not available",
            "request_data": {
                "prompt_name": prompt_name,
                "prompt_length": len(prompt) if prompt else 0,
                "lora": lora,
                "style_strength": style_strength
            },
            "service_status": {
                "comfy_url": COMFY_URL,
                "comfy_available": comfy_available
            }
        }
        logger.error(f"ComfyUI is not available for single lora generation: {json.dumps(error_detail, indent=2)}")
        raise RuntimeError("ComfyUI is not available")
        
    prompt_name = file_utils.sanitize_filename(prompt_name)
    clean_prompt_name = prompt_name.replace(".txt", "")
    try:
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
                sigmas = BasicScheduler(model, "simple", 1, 1)
                latent = EmptyLatentImage(1088, 1088, 1)
                latent, _ = SamplerCustomAdvanced(noise, guider, sampler, sigmas, latent)
                vae = VAELoader("ae.safetensors")
                image = VAEDecode(latent, vae)
                lora = file_utils.sanitize_filename(lora)
                clean_lora_name = lora.replace(".safetensors", "")
                filename = f"{clean_prompt_name}_{clean_lora_name}_{n}.png"
                image_64 = SaveImage(image, "ComfyUI")
                def safe_get_str(value):
                    import io, contextlib
                    sio = io.StringIO()
                    with contextlib.redirect_stdout(sio):
                        return util.get_str(value)
                img_str = util.get_str(image_64)
                img_str = clean_base64(img_str)
                return filename, img_str
    except Exception as e:
        error_detail = {
            "error_code": "COMFY_GENERATION_ERROR",
            "message": f"Error generating image with single lora: {str(e)}",
            "request_data": {
                "prompt_name": prompt_name,
                "prompt_length": len(prompt) if prompt else 0,
                "lora": lora,
                "style_strength": style_strength
            },
            "service_status": {
                "comfy_url": COMFY_URL,
                "comfy_available": comfy_available
            }
        }
        logger.error(f"ComfyUI generation error: {json.dumps(error_detail, indent=2)}")
        raise RuntimeError(f"Error generating image with ComfyUI: {str(e)}")


def comfy_call_stacked_lora(prompt_name, prompt, lora_list, batch_size):
    """Function to call stacked loras"""
    if not check_comfy_available():
        error_detail = {
            "error_code": "COMFY_UNAVAILABLE",
            "message": "ComfyUI is not available",
            "request_data": {
                "prompt_name": prompt_name,
                "prompt_length": len(prompt) if prompt else 0,
                "lora_count": len(lora_list) if lora_list else 0,
                "batch_size": batch_size
            },
            "service_status": {
                "comfy_url": COMFY_URL,
                "comfy_available": comfy_available
            }
        }
        logger.error(f"ComfyUI is not available for stacked lora call: {json.dumps(error_detail, indent=2)}")
        raise RuntimeError("ComfyUI is not available")
        
    results = []
    for i in range(batch_size):
        filename, img_str = stacked_lora(prompt_name, prompt, lora_list)
        results.append({"filename": filename, "data": img_str})
    return results


def stacked_lora(prompt_name, prompt, lora_list):
    if not check_comfy_available():
        error_detail = {
            "error_code": "COMFY_UNAVAILABLE",
            "message": "ComfyUI is not available",
            "request_data": {
                "prompt_name": prompt_name,
                "prompt_length": len(prompt) if prompt else 0,
                "lora_count": len(lora_list) if lora_list else 0
            },
            "service_status": {
                "comfy_url": COMFY_URL,
                "comfy_available": comfy_available
            }
        }
        logger.error(f"ComfyUI is not available for stacked lora generation: {json.dumps(error_detail, indent=2)}")
        raise RuntimeError("ComfyUI is not available")
        
    prompt_name = file_utils.sanitize_filename(prompt_name)
    clean_prompt_name = prompt_name.replace(".txt", "")
    try:
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
    except Exception as e:
        error_detail = {
            "error_code": "COMFY_GENERATION_ERROR",
            "message": f"Error generating image with stacked lora: {str(e)}",
            "request_data": {
                "prompt_name": prompt_name,
                "prompt_length": len(prompt) if prompt else 0,
                "lora_count": len(lora_list) if lora_list else 0
            },
            "service_status": {
                "comfy_url": COMFY_URL,
                "comfy_available": comfy_available
            }
        }
        logger.error(f"ComfyUI generation error: {json.dumps(error_detail, indent=2)}")
        raise RuntimeError(f"Error generating image with ComfyUI: {str(e)}")


def comfy_call_single_art(prompt_name, prompt, art, batch_size):
    """Function to call single art"""
    if not check_comfy_available():
        error_detail = {
            "error_code": "COMFY_UNAVAILABLE",
            "message": "ComfyUI is not available",
            "request_data": {
                "prompt_name": prompt_name,
                "prompt_length": len(prompt) if prompt else 0,
                "art": art,
                "batch_size": batch_size
            },
            "service_status": {
                "comfy_url": COMFY_URL,
                "comfy_available": comfy_available
            }
        }
        logger.error(f"ComfyUI is not available for single art call: {json.dumps(error_detail, indent=2)}")
        raise RuntimeError("ComfyUI is not available")
        
    results = []
    for i in range(batch_size):
        filename, img_str = single_art(prompt_name, prompt, art)
        results.append({"filename": filename, "data": img_str})
    return results


def single_art(prompt_name, prompt, art):
    if not check_comfy_available():
        error_detail = {
            "error_code": "COMFY_UNAVAILABLE",
            "message": "ComfyUI is not available",
            "request_data": {
                "prompt_name": prompt_name,
                "prompt_length": len(prompt) if prompt else 0,
                "art": art
            },
            "service_status": {
                "comfy_url": COMFY_URL,
                "comfy_available": comfy_available
            }
        }
        logger.error(f"ComfyUI is not available for single art generation: {json.dumps(error_detail, indent=2)}")
        raise RuntimeError("ComfyUI is not available")
        
    prompt_name = file_utils.sanitize_filename(prompt_name)
    clean_prompt_name = prompt_name.replace(".txt", "")
    try:
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
    except Exception as e:
        error_detail = {
            "error_code": "COMFY_GENERATION_ERROR",
            "message": f"Error generating image with single art: {str(e)}",
            "request_data": {
                "prompt_name": prompt_name,
                "prompt_length": len(prompt) if prompt else 0,
                "art": art
            },
            "service_status": {
                "comfy_url": COMFY_URL,
                "comfy_available": comfy_available
            }
        }
        logger.error(f"ComfyUI generation error: {json.dumps(error_detail, indent=2)}")
        raise RuntimeError(f"Error generating image with ComfyUI: {str(e)}")


def comfy_call_stacked_art(prompt_name, prompt, batch_size):
    """Function to call stacked arts"""
    if not check_comfy_available():
        error_detail = {
            "error_code": "COMFY_UNAVAILABLE",
            "message": "ComfyUI is not available",
            "request_data": {
                "prompt_name": prompt_name,
                "prompt_length": len(prompt) if prompt else 0,
                "batch_size": batch_size
            },
            "service_status": {
                "comfy_url": COMFY_URL,
                "comfy_available": comfy_available
            }
        }
        logger.error(f"ComfyUI is not available for stacked art call: {json.dumps(error_detail, indent=2)}")
        raise RuntimeError("ComfyUI is not available")
        
    results = []
    for i in range(batch_size):
        filename, img_str = stacked_art(prompt_name, prompt)
        results.append({"filename": filename, "data": img_str})
    return results


def stacked_art(prompt_name, prompt):
    if not check_comfy_available():
        error_detail = {
            "error_code": "COMFY_UNAVAILABLE",
            "message": "ComfyUI is not available",
            "request_data": {
                "prompt_name": prompt_name,
                "prompt_length": len(prompt) if prompt else 0
            },
            "service_status": {
                "comfy_url": COMFY_URL,
                "comfy_available": comfy_available
            }
        }
        logger.error(f"ComfyUI is not available for stacked art generation: {json.dumps(error_detail, indent=2)}")
        raise RuntimeError("ComfyUI is not available")
        
    prompt_name = file_utils.sanitize_filename(prompt_name)
    clean_prompt_name = prompt_name.replace(".txt", "")
    try:
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
    except Exception as e:
        error_detail = {
            "error_code": "COMFY_GENERATION_ERROR",
            "message": f"Error generating image with stacked art: {str(e)}",
            "request_data": {
                "prompt_name": prompt_name,
                "prompt_length": len(prompt) if prompt else 0
            },
            "service_status": {
                "comfy_url": COMFY_URL,
                "comfy_available": comfy_available
            }
        }
        logger.error(f"ComfyUI generation error: {json.dumps(error_detail, indent=2)}")
        raise RuntimeError(f"Error generating image with ComfyUI: {str(e)}")


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
