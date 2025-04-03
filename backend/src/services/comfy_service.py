# For comfyui
from comfy_script.runtime import *

load("http://127.0.0.1:8188/")
from comfy_script.runtime.nodes import *
from comfy_script.runtime import util


def comfy_single_style(prompt, lora, seed, style_strength):
    with Workflow():
        model, clip, vae = CheckpointLoaderSimple(
            "juggernautXL_v8Rundiffusion.safetensors"
        )
        if lora:
            model, clip = LoraLoader(model, clip, lora, style_strength, 1)
        conditioning = CLIPTextEncode(prompt, clip)
        conditioning2 = CLIPTextEncode("text, watermark", clip)
        latent = EmptyLatentImage(1024, 1024, 1)
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


def comfy_stacked_style(prompt, lora_list, seed):
    with Workflow():
        model, clip, vae = CheckpointLoaderSimple(
            "juggernautXL_v8Rundiffusion.safetensors"
        )
        if lora_list:
            for l in lora_list:
                model, clip = LoraLoader(model, clip, l["id"], l["styleStrength"], 1)
        conditioning = CLIPTextEncode(prompt, clip)
        conditioning2 = CLIPTextEncode("text, watermark", clip)
        # Generate base image first before resizing it
        latent = EmptyLatentImage(1024, 1024, 1)
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


def single_style_str(prompt, lora, seed, batch_size, style_strength, ratio):
    results = []
    for i in range(batch_size):
        current_seed = seed + i
        img = comfy_single_style(prompt, lora, current_seed, style_strength)
        img_str = util.get_str(img)
        print("Single style generating for: ", lora)
        final_img = resize_workflow(img_str, ratio)
        final_str = util.get_str(final_img)
        results.append(final_str)
    return results


def stacked_style_str(prompt, lora_list, seed, batch_size, ratio):
    results = []
    for i in range(batch_size):
        current_seed = seed + i
        img = comfy_stacked_style(prompt, lora_list, current_seed)
        img_str = util.get_str(img)
        print("Stacked style generating for: ", lora_list)
        final_img = resize_workflow(img_str, ratio)
        final_str = util.get_str(final_img)
        results.append(final_str)
    return results


def resize_workflow(img_str, ratio):
    with Workflow():
        model = UnetLoaderGGUF("flux1-fill-dev-Q4_K_S.gguf")
        model = DifferentialDiffusion(model)
        clip = DualCLIPLoader(
            "clip_l.safetensors", "t5xxl_fp8_e4m3fn.safetensors", "flux", "default"
        )
        model2, processor = JanusModelLoader("deepseek-ai/Janus-Pro-1B")
        image, _ = EasyLoadImageBase64(img_str)
        text = JanusImageUnderstanding(
            model2,
            processor,
            image,
            "用英文描述一下这张图片的背景，只描述背景，只描述背景，不要出现任何人物描述",
            794902560779472,
            0.1,
            1,
            512,
        )
        text = ShowTextPysssss(text)
        conditioning = CLIPTextEncode(text, clip)
        conditioning = FluxGuidance(conditioning, 30)
        conditioning2 = CLIPTextEncode(
            "There are watermark and texts on the images.There are people, there are many people",
            clip,
        )
        conditioning2 = FluxGuidance(conditioning2, 30)
        vae = VAELoader("ae.safetensors")
        image2 = JWImageResizeByLongerSide(image, 1080, "bicubic")
        width_extension_per_side, height_extension_per_side = (
            CalculateAspectRatioExtension(image2, "1:1", 1, 1)
        )
        image3, mask = ExtendCanvasByPercentage(
            image2,
            False,
            True,
            height_extension_per_side,
            height_extension_per_side,
            width_extension_per_side,
            width_extension_per_side,
            0,
            "#7f7f7f",
            None,
        )
        image3, mask = ExtendCanvasByPercentage(
            image3, True, False, 5, 0, 8, 8, 8, "#7f7f7f", mask
        )
        positive, negative, latent = InpaintModelConditioning(
            conditioning, conditioning2, vae, image3, mask, False
        )
        latent = KSampler(
            model,
            785164945698779,
            20,
            3.5,
            "euler",
            "normal",
            positive,
            negative,
            latent,
            1,
        )
        image4 = VAEDecode(latent, vae)
        if ratio == "1:1":
            cropped_image, _, _ = ImageCropByPercentage(
                False, image4, 80, 80, "top-center", 0, 0
            )
            cropped_image = JWImageResizeByShorterSide(cropped_image, 1080, "bicubic")
            cropped_image, _, _ = ImageCropByPercentage(
                True, cropped_image, 1080, 1080, "top-center", 0, 0
            )
            return SaveImage(cropped_image, "ComfyUI")
        elif ratio == "16:9":
            upscale_model = UpscaleModelLoader("RealESRGAN_x4plus.pth")
            _, mask2 = LayerMaskTransparentBackgroundUltra(
                image4,
                "ckpt_base.pth",
                "VITMatte",
                6,
                6,
                0.010000000000000002,
                0.99,
                True,
                "cuda",
                2,
            )
            cropped_image, _, _, _ = MaskCropByPercentage(
                image4, mask2, False, False, "mask_area", 20, 20, 20, 20, "8", None
            )
            _, mask3 = LayerMaskSegmentAnythingUltraV2(
                cropped_image,
                "sam_vit_l (1.25GB)",
                "GroundingDINO_SwinT_OGC (694MB)",
                0.30000000000000004,
                "VITMatte",
                6,
                6,
                0.15000000000000002,
                0.99,
                True,
                "face",
                "cuda",
                2,
                False,
            )
            cropped_image2, _, _, _ = MaskCropByPercentage(
                cropped_image,
                mask3,
                False,
                False,
                "mask_area",
                10,
                50,
                50,
                50,
                "8",
                None,
            )
            cropped_image2 = UpscaleByFactorWithModelWLSH(
                upscale_model, cropped_image2, "nearest-exact", 1.5
            )
            cropped_image2 = JWImageResizeByLongerSide(cropped_image2, 1920, "bicubic")
            cropped_image2, _, _ = ImageCropEssential(
                cropped_image2, 1920, 1080, "top-center", 0, 0
            )
            return SaveImage(cropped_image2, "ComfyUI")
        elif ratio == "9:16":
            upscale_model = UpscaleModelLoader("RealESRGAN_x4plus.pth")
            _, mask2 = LayerMaskSegmentAnythingUltraV2(
                image4,
                "sam_vit_l (1.25GB)",
                "GroundingDINO_SwinT_OGC (694MB)",
                0.30000000000000004,
                "VITMatte",
                6,
                6,
                0.15000000000000002,
                0.99,
                True,
                "face",
                "cuda",
                2,
                False,
            )
            cropped_image, _, _, _ = MaskCropByPercentage(
                image4, mask2, False, False, "mask_area", 20, 50, 40, 40, "8", None
            )
            cropped_image = UpscaleByFactorWithModelWLSH(
                upscale_model, cropped_image, "nearest-exact", 1.8
            )
            cropped_image = JWImageResizeByShorterSide(cropped_image, 1920, "bicubic")
            cropped_image, _, _ = ImageCropEssential(
                cropped_image, 1080, 1920, "top-center", 0, 0
            )
            return SaveImage(cropped_image, "ComfyUI")
        else:
            raise ValueError("Invalid aspect ratio in resize_workflow")
