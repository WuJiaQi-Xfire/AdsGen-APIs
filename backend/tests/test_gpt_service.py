import pytest
from src.services import gpt_service
import base64

def test_create_prompt():
    """Test prompt creation with text description"""
    description = "A beautiful landscape with mountains and a lake"
    prompt = gpt_service.create_prompt(description)
    
    assert prompt is not None
    assert isinstance(prompt, str)
    assert len(prompt) > 0

def test_create_prompt_with_image():
    """Test prompt creation with image"""
    description = "Describe the contents of this image"
    
    # Create a simple base64 encoded test image
    test_image = base64.b64encode(b'test image content').decode('utf-8')
    
    prompt = gpt_service.create_prompt(description, test_image)
    
    assert prompt is not None
    assert isinstance(prompt, str)
    assert len(prompt) > 0

def test_extract_keywords():
    """Test keyword extraction"""
    description = "A vibrant cityscape at night"
    
    keywords = gpt_service.extract_keywords(description)
    
    assert keywords is not None
    assert isinstance(keywords, str)
    assert len(keywords) > 0

def test_create_prompt_error_handling():
    """Test error handling for prompt creation"""
    with pytest.raises(ValueError):
        gpt_service.create_prompt("")  # Empty description should raise an error
