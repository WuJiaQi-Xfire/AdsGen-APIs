import os
import base64

# For comfyui
from comfy_script.runtime import *

load("http://127.0.0.1:8188/")
from comfy_script.runtime.nodes import *
from comfy_script.runtime import util

# Locally for now
file_path = r"C:\Users\GT0730-1\Documents\GitHub\Ads-Gen\Output\base_image"
preview_path = r"C:\Users\GT0730-1\Documents\GitHub\Ads-Gen\Output\resized_image"


def comfy_call_single_lora(
    prompt_name, prompt, lora, seed, batch_size, style_strength, ratio
):
    for i in range(batch_size):
        single_lora(prompt_name, prompt, lora, seed, style_strength, ratio)


def single_lora(
    prompt_name, prompt, lora, seed, style_strength, ratio
):
    clean_prompt_name = prompt_name.replace(".txt", "")
    clean_lora_name = lora.replace(".safetensors", "")

    with Workflow():
        noise = RandomNoise(119501675105851)
        model, _, _ = CheckpointLoaderSimple('flux1-dev-fp8.safetensors')
        clip = DualCLIPLoader('t5xxl_fp8_e4m3fn.safetensors', 'clip_l.safetensors', 'flux', 'default')
        model, clip = LoraLoader(model, clip, lora, style_strength, 1)
        model = ModelSamplingFlux(model, 1.12, 0.5000000000000001, 1024, 1024)
        clip_text_encode_positive_prompt_conditioning = CLIPTextEncode(prompt, clip)
        clip_text_encode_positive_prompt_conditioning = FluxGuidance(clip_text_encode_positive_prompt_conditioning, 3.5)
        guider = BasicGuider(model, clip_text_encode_positive_prompt_conditioning)
        sampler = KSamplerSelect('euler')
        sigmas = BasicScheduler(model, 'simple', 20, 1)
        latent = EmptyLatentImage(1080, 1080, 1)
        latent, _ = SamplerCustomAdvanced(noise, guider, sampler, sigmas, latent)
        vae = VAELoader('ae.safetensors')
        image = VAEDecode(latent, vae)
        filename = f"{clean_prompt_name}_{clean_lora_name}_{seed}"
        _, _ = GregSaveImageWithSuffix(
            image,
            True,
            file_path,
            filename,
            "_",
            "",
            4,
            "false",
            "true",
            "png",
            300,
            100,
            "true",
            "false",
            "false",
            "false",
            "false",
            "true",
            "false",
        )
        model2 = UnetLoaderGGUF("flux1-fill-dev-Q4_K_S.gguf")
        model2 = DifferentialDiffusion(model2)
        model3, processor = JanusModelLoader("deepseek-ai/Janus-Pro-1B")
        text = JanusImageUnderstanding(
            model3,
            processor,
            image,
            "用英文描述一下这张图片的背景，只描述背景，只描述背景，不要出现任何人物描述",
            794902560779472,
            0.1,
            1,
            512,
        )
        conditioning = CLIPTextEncode(text, clip)
        conditioning = FluxGuidance(conditioning, 30)
        conditioning2 = CLIPTextEncode(
            "There are watermark and texts on the images.There are people, there are many people",
            clip,
        )
        conditioning2 = FluxGuidance(conditioning2, 30)
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
            model2,
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
        upscale_model = UpscaleModelLoader("RealESRGAN_x4plus.pth")
        if ratio == "16:9":
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
            new_filename = f"{filename}_16_9"
            _, _ = GregSaveImageWithSuffix(
                cropped_image2,
                True,
                preview_path,
                new_filename,
                "_",
                "",
                4,
                "false",
                "true",
                "png",
                300,
                100,
                "true",
                "false",
                "false",
                "false",
                "false",
                "true",
                "false",
            )
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
            new_filename = f"{filename}_9_16"
            _, _ = GregSaveImageWithSuffix(
                cropped_image,
                True,
                preview_path,
                new_filename,
                "_",
                "",
                4,
                "false",
                "true",
                "png",
                300,
                100,
                "true",
                "false",
                "false",
                "false",
                "false",
                "true",
                "false",
            )


def comfy_call_stacked_lora(prompt_name, prompt, lora_list, seed, batch_size, ratio):
    for i in range(batch_size):
        stacked_lora(prompt_name, prompt, lora_list, seed, ratio)


def stacked_lora(prompt_name, prompt, lora_list, seed, ratio):
    clean_prompt_name = prompt_name.replace(".txt", "")
    with Workflow():
        noise = RandomNoise(119501675105851)
        model, _, _ = CheckpointLoaderSimple('flux1-dev-fp8.safetensors')
        clip = DualCLIPLoader('t5xxl_fp8_e4m3fn.safetensors', 'clip_l.safetensors', 'flux', 'default')
        for l in lora_list:
            model, clip = LoraLoader(model, clip, l["id"], l["styleStrength"], 1)
        model = ModelSamplingFlux(model, 1.12, 0.5000000000000001, 1024, 1024)
        clip_text_encode_positive_prompt_conditioning = CLIPTextEncode(prompt, clip)
        clip_text_encode_positive_prompt_conditioning = FluxGuidance(clip_text_encode_positive_prompt_conditioning, 3.5)
        guider = BasicGuider(model, clip_text_encode_positive_prompt_conditioning)
        sampler = KSamplerSelect('euler')
        sigmas = BasicScheduler(model, 'simple', 20, 1)
        latent = EmptyLatentImage(1080, 1080, 1)
        latent, _ = SamplerCustomAdvanced(noise, guider, sampler, sigmas, latent)
        vae = VAELoader('ae.safetensors')
        image = VAEDecode(latent, vae)
        filename = f"{clean_prompt_name}_stacked_lora_{seed}"
        _, _ = GregSaveImageWithSuffix(
            image,
            True,
            file_path,
            filename,
            "_",
            "",
            4,
            "false",
            "true",
            "png",
            300,
            100,
            "true",
            "false",
            "false",
            "false",
            "false",
            "true",
            "false",
        )
        model2 = UnetLoaderGGUF("flux1-fill-dev-Q4_K_S.gguf")
        model2 = DifferentialDiffusion(model2)
        model3, processor = JanusModelLoader("deepseek-ai/Janus-Pro-1B")
        text = JanusImageUnderstanding(
            model3,
            processor,
            image,
            "用英文描述一下这张图片的背景，只描述背景，只描述背景，不要出现任何人物描述",
            794902560779472,
            0.1,
            1,
            512,
        )
        conditioning = CLIPTextEncode(text, clip)
        conditioning = FluxGuidance(conditioning, 30)
        conditioning2 = CLIPTextEncode(
            "There are watermark and texts on the images.There are people, there are many people",
            clip,
        )
        conditioning2 = FluxGuidance(conditioning2, 30)
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
            model2,
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
        upscale_model = UpscaleModelLoader("RealESRGAN_x4plus.pth")
        if ratio == "16:9":
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
            new_filename = f"{filename}_16_9"
            _, _ = GregSaveImageWithSuffix(
                cropped_image2,
                True,
                preview_path,
                new_filename,
                "_",
                "",
                4,
                "false",
                "true",
                "png",
                300,
                100,
                "true",
                "false",
                "false",
                "false",
                "false",
                "true",
                "false",
            )
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
            new_filename = f"{filename}_9_16"
            _, _ = GregSaveImageWithSuffix(
                cropped_image,
                True,
                preview_path,
                new_filename,
                "_",
                "",
                4,
                "false",
                "true",
                "png",
                300,
                100,
                "true",
                "false",
                "false",
                "false",
                "false",
                "true",
                "false",
            )

def comfy_call_single_art(
    prompt_name, prompt, art, seed, batch_size, ratio
):
    for i in range(batch_size):
        single_art(prompt_name, prompt, art, seed, ratio)


def single_art(
    prompt_name, prompt, art, seed,  ratio
):
    clean_prompt_name = prompt_name.replace(".txt", "")
    with Workflow():
        noise = RandomNoise(313190674711926)
        model = UNETLoader('flux1-dev-fp8.safetensors', 'default')
        model = ModelSamplingFlux(model, 1.12, 0.5000000000000001, 1024, 1024)
        clip = DualCLIPLoader('t5xxl_fp8_e4m3fn.safetensors', 'clip_l.safetensors', 'flux', 'default')
        clip_text_encode_positive_prompt_conditioning = CLIPTextEncode(prompt, clip)
        clip_text_encode_positive_prompt_conditioning = FluxGuidance(clip_text_encode_positive_prompt_conditioning, 3.5)
        guider = BasicGuider(model, clip_text_encode_positive_prompt_conditioning)
        sampler = KSamplerSelect('euler')
        sigmas = BasicScheduler(model, 'simple', 20, 1)
        latent = EmptyLatentImage(1080, 1080, 1)
        latent, _ = SamplerCustomAdvanced(noise, guider, sampler, sigmas, latent)
        vae = VAELoader('ae.safetensors')
        image = VAEDecode(latent, vae)
        filename = f"{clean_prompt_name}_{art}_{seed}"
        _, _ = GregSaveImageWithSuffix(
            image,
            True,
            file_path,
            filename,
            "_",
            "",
            4,
            "false",
            "true",
            "png",
            300,
            100,
            "true",
            "false",
            "false",
            "false",
            "false",
            "true",
            "false",
        )
        model2 = UnetLoaderGGUF("flux1-fill-dev-Q4_K_S.gguf")
        model2 = DifferentialDiffusion(model2)
        model3, processor = JanusModelLoader("deepseek-ai/Janus-Pro-1B")
        text = JanusImageUnderstanding(
            model3,
            processor,
            image,
            "用英文描述一下这张图片的背景，只描述背景，只描述背景，不要出现任何人物描述",
            794902560779472,
            0.1,
            1,
            512,
        )
        conditioning = CLIPTextEncode(text, clip)
        conditioning = FluxGuidance(conditioning, 30)
        conditioning2 = CLIPTextEncode(
            "There are watermark and texts on the images.There are people, there are many people",
            clip,
        )
        conditioning2 = FluxGuidance(conditioning2, 30)
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
        positive, negative, latent2 = InpaintModelConditioning(
            conditioning, conditioning2, vae, image3, mask, False
        )
        latent2 = KSampler(
            model3,
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
        image4 = VAEDecode(latent2, vae)
        upscale_model = UpscaleModelLoader("RealESRGAN_x4plus.pth")
        if ratio == "16:9":
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
            new_filename = f"{filename}_16_9"
            _, _ = GregSaveImageWithSuffix(
                cropped_image2,
                True,
                preview_path,
                new_filename,
                "_",
                "",
                4,
                "false",
                "true",
                "png",
                300,
                100,
                "true",
                "false",
                "false",
                "false",
                "false",
                "true",
                "false",
            )
        elif ratio == "9:16":
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
            new_filename = f"{filename}_9_16"
            _, _ = GregSaveImageWithSuffix(
                cropped_image,
                True,
                preview_path,
                new_filename,
                "_",
                "",
                4,
                "false",
                "true",
                "png",
                300,
                100,
                "true",
                "false",
                "false",
                "false",
                "false",
                "true",
                "false",
            )

def comfy_call_stacked_art(prompt_name, prompt, seed, batch_size, ratio):
    for i in range(batch_size):
        stacked_art(prompt_name, prompt, seed, ratio)


def stacked_art(prompt_name, prompt, seed, ratio):
    clean_prompt_name = prompt_name.replace(".txt", "")
    with Workflow():
        noise = RandomNoise(313190674711926)
        model = UNETLoader('flux1-dev-fp8.safetensors', 'default')
        model = ModelSamplingFlux(model, 1.12, 0.5000000000000001, 1024, 1024)
        clip = DualCLIPLoader('t5xxl_fp8_e4m3fn.safetensors', 'clip_l.safetensors', 'flux', 'default')
        clip_text_encode_positive_prompt_conditioning = CLIPTextEncode(prompt, clip)
        clip_text_encode_positive_prompt_conditioning = FluxGuidance(clip_text_encode_positive_prompt_conditioning, 3.5)
        guider = BasicGuider(model, clip_text_encode_positive_prompt_conditioning)
        sampler = KSamplerSelect('euler')
        sigmas = BasicScheduler(model, 'simple', 20, 1)
        latent = EmptyLatentImage(1080, 1080, 1)
        latent, _ = SamplerCustomAdvanced(noise, guider, sampler, sigmas, latent)
        vae = VAELoader('ae.safetensors')
        image = VAEDecode(latent, vae)
        filename = f"{clean_prompt_name}_stacked_art_{seed}"
        _, _ = GregSaveImageWithSuffix(
            image,
            True,
            file_path,
            filename,
            "_",
            "",
            4,
            "false",
            "true",
            "png",
            300,
            100,
            "true",
            "false",
            "false",
            "false",
            "false",
            "true",
            "false",
        )
        model2 = UnetLoaderGGUF("flux1-fill-dev-Q4_K_S.gguf")
        model2 = DifferentialDiffusion(model2)
        model3, processor = JanusModelLoader("deepseek-ai/Janus-Pro-1B")
        text = JanusImageUnderstanding(
            model3,
            processor,
            image,
            "用英文描述一下这张图片的背景，只描述背景，只描述背景，不要出现任何人物描述",
            794902560779472,
            0.1,
            1,
            512,
        )
        conditioning = CLIPTextEncode(text, clip)
        conditioning = FluxGuidance(conditioning, 30)
        conditioning2 = CLIPTextEncode(
            "There are watermark and texts on the images.There are people, there are many people",
            clip,
        )
        conditioning2 = FluxGuidance(conditioning2, 30)
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
        positive, negative, latent2 = InpaintModelConditioning(
            conditioning, conditioning2, vae, image3, mask, False
        )
        latent2 = KSampler(
            model3,
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
        image4 = VAEDecode(latent2, vae)
        upscale_model = UpscaleModelLoader("RealESRGAN_x4plus.pth")
        if ratio == "16:9":
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
            new_filename = f"{filename}_16_9"
            _, _ = GregSaveImageWithSuffix(
                cropped_image2,
                True,
                preview_path,
                new_filename,
                "_",
                "",
                4,
                "false",
                "true",
                "png",
                300,
                100,
                "true",
                "false",
                "false",
                "false",
                "false",
                "true",
                "false",
            )
        elif ratio == "9:16":
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
            new_filename = f"{filename}_9_16"
            _, _ = GregSaveImageWithSuffix(
                cropped_image,
                True,
                preview_path,
                new_filename,
                "_",
                "",
                4,
                "false",
                "true",
                "png",
                300,
                100,
                "true",
                "false",
                "false",
                "false",
                "false",
                "true",
                "false",
            )

def get_generated_images():
    """Load all images from the resized_image folder and convert them to base64 strings."""
    images = []
    try:
        image_files = [f for f in os.listdir(preview_path) if f.lower().endswith((".png"))]

        for image_file in image_files:
            new_path = os.path.join(preview_path, image_file)
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
