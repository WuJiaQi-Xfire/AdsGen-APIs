import json
import base64
from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)

def test_generate_prompt_endpoint():
    """Test the generate-prompt endpoint"""
    # Prepare test data
    test_data = {
        "description": "A serene mountain landscape",
        "image_url": None
    }
    
    response = client.post("/generate-prompt/", data=test_data)
    
    assert response.status_code == 200
    response_data = response.json()
    
    assert 'generated_prompt' in response_data
    assert isinstance(response_data['generated_prompt'], str)
    assert len(response_data['generated_prompt']) > 0

def test_extract_keywords_endpoint():
    """Test the extract-keywords endpoint"""
    # Prepare test data
    test_data = {
        "description": "A vibrant cityscape at night"
    }
    
    response = client.post("/extract-keywords/", data=test_data)
    
    assert response.status_code == 200
    response_data = response.json()
    
    assert 'keywords' in response_data
    assert isinstance(response_data['keywords'], str)
    assert len(response_data['keywords']) > 0

def test_get_styles_endpoint():
    """Test the get-styles endpoint"""
    response = client.get("/get-styles/")
    
    assert response.status_code == 200
    response_data = response.json()
    
    assert 'loraStyles' in response_data
    assert 'artStyles' in response_data
    
    assert isinstance(response_data['loraStyles'], list)
    assert isinstance(response_data['artStyles'], list)

def test_generate_image_endpoint():
    """Test the generate-image endpoint"""
    # Prepare test data
    test_data = {
        "prompts": json.dumps([{
            "name": "Test Prompt",
            "content": "A futuristic cityscape"
        }]),
        "style_settings": json.dumps([{
            "id": "test_lora",
            "styleType": "lora",
            "styleStrength": 0.7,
            "batchSize": 1,
            "aspectRatio": "16:9"
        }]),
        "keywords": "futuristic, city, night",
        "stack_loras": "false"
    }
    
    response = client.post("/generate-image/", data=test_data)
    
    assert response.status_code == 200
    response_data = response.json()
    
    assert 'images' in response_data
    assert isinstance(response_data['images'], list)
