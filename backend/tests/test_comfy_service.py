import pytest
import os
from src.services import comfy_service, file_service

def test_get_generated_images():
    """Test retrieving generated images"""
    # Ensure image folders exist
    os.makedirs(comfy_service.preview_path, exist_ok=True)
    os.makedirs(comfy_service.output_path, exist_ok=True)
    
    # Clear existing images
    file_service.clear_image_folders()
    
    # Simulate image generation by creating test images
    test_image_paths = [
        os.path.join(comfy_service.output_path, f'test_image_{i}.png') 
        for i in range(3)
    ]
    
    for path in test_image_paths:
        with open(path, 'wb') as f:
            f.write(b'test image content')
    
    # Get generated images
    generated_images = comfy_service.get_generated_images()
    
    # Clean up test images
    for path in test_image_paths:
        os.remove(path)
    
    # Assertions
    assert isinstance(generated_images, list)
    assert len(generated_images) > 0
    
    # Check image details
    for image in generated_images:
        assert 'url' in image
        assert 'filename' in image

def test_comfy_call_single_lora():
    """Test single Lora style image generation call"""
    prompt_name = "Test Prompt"
    prompt = "A beautiful landscape"
    lora_id = "test_lora"
    batch_size = 1
    style_strength = 0.7
    aspect_ratio = "16:9"
    
    try:
        result = comfy_service.comfy_call_single_lora(
            prompt_name, prompt, lora_id, 
            batch_size, style_strength, aspect_ratio
        )
        assert result is not None
    except Exception as e:
        pytest.fail(f"Comfy call failed: {str(e)}")

def test_comfy_call_stacked_lora():
    """Test stacked Lora style image generation call"""
    prompt_name = "Test Stacked Prompt"
    prompt = "A futuristic cityscape"
    lora_list = [
        {"id": "lora1", "styleStrength": 0.5},
        {"id": "lora2", "styleStrength": 0.5}
    ]
    batch_size = 2
    aspect_ratio = "16:9"
    
    try:
        result = comfy_service.comfy_call_stacked_lora(
            prompt_name, prompt, lora_list, 
            batch_size, aspect_ratio
        )
        assert result is not None
    except Exception as e:
        pytest.fail(f"Comfy stacked call failed: {str(e)}")

def test_preview_path_exists():
    """Verify preview path exists and is accessible"""
    assert os.path.exists(comfy_service.preview_path)
    assert os.path.isdir(comfy_service.preview_path)
    assert os.access(comfy_service.preview_path, os.R_OK | os.W_OK)
