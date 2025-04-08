from fastapi.testclient import TestClient
from src.main import app
import json

client = TestClient(app)

def test_create_prompt():
    """Test creating a new prompt via API"""
    # Prepare prompt data
    prompt_data = {
        "prompt_name": "API Test Prompt",
        "content": "This is a test prompt created via API"
    }
    
    # Send POST request to create prompt
    response = client.post("/prompts/", json=prompt_data)
    
    # Check response
    assert response.status_code == 200
    response_data = response.json()
    
    # Verify response contains prompt ID
    assert 'id' in response_data
    assert 'message' in response_data
    assert response_data['message'] == "Prompt saved successfully"

def test_get_prompts():
    """Test retrieving all prompts"""
    # First, create a prompt to ensure we have data
    prompt_data = {
        "prompt_name": "Retrieval Test Prompt",
        "content": "This prompt is for testing retrieval"
    }
    client.post("/prompts/", json=prompt_data)
    
    # Get all prompts
    response = client.get("/prompts/")
    
    # Check response
    assert response.status_code == 200
    prompts = response.json()
    
    # Verify prompts are returned
    assert isinstance(prompts, list)
    assert len(prompts) > 0
    
    # Check prompt structure
    sample_prompt = prompts[0]
    assert 'id' in sample_prompt
    assert 'prompt_name' in sample_prompt
    assert 'content' in sample_prompt
    assert 'created_at' in sample_prompt

def test_get_specific_prompt():
    """Test retrieving a specific prompt by ID"""
    # First, create a prompt
    prompt_data = {
        "prompt_name": "Specific Prompt",
        "content": "This is a prompt to test specific retrieval"
    }
    create_response = client.post("/prompts/", json=prompt_data)
    prompt_id = create_response.json()['id']
    
    # Retrieve the specific prompt
    response = client.get(f"/prompts/{prompt_id}")
    
    # Check response
    assert response.status_code == 200
    prompt = response.json()
    
    # Verify prompt details
    assert prompt['id'] == prompt_id
    assert prompt['prompt_name'] == "Specific Prompt"
    assert prompt['content'] == "This is a prompt to test specific retrieval"

def test_delete_prompt():
    """Test deleting a prompt"""
    # First, create a prompt
    prompt_data = {
        "prompt_name": "Prompt to Delete",
        "content": "This prompt will be deleted via API"
    }
    create_response = client.post("/prompts/", json=prompt_data)
    prompt_id = create_response.json()['id']
    
    # Delete the prompt
    delete_response = client.delete(f"/prompts/{prompt_id}")
    
    # Check response
    assert delete_response.status_code == 200
    
    # Try to retrieve the deleted prompt
    get_response = client.get(f"/prompts/{prompt_id}")
    
    # Verify the prompt is no longer accessible
    assert get_response.status_code == 404
