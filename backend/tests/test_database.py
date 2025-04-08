import pytest
from datetime import datetime

def test_save_and_retrieve_prompt(db_manager):
    """Test saving and retrieving a prompt"""
    # Save a prompt
    prompt_name = "Test Prompt"
    prompt_content = "This is a test prompt content"
    prompt_id = db_manager.save_prompt(prompt_name, prompt_content)
    
    # Verify the prompt was saved
    assert prompt_id is not None
    assert isinstance(prompt_id, int)
    
    # Retrieve the prompt
    prompt = db_manager.get_prompt(prompt_id)
    
    # Check prompt details
    assert prompt is not None
    assert prompt['prompt_name'] == prompt_name
    assert prompt['content'] == prompt_content
    assert 'created_at' in prompt
    assert isinstance(prompt['created_at'], datetime)

def test_list_prompts(db_manager):
    """Test listing multiple prompts"""
    # Save multiple prompts
    prompt_names = ["Prompt 1", "Prompt 2", "Prompt 3"]
    prompt_contents = ["Content 1", "Content 2", "Content 3"]
    
    saved_ids = []
    for name, content in zip(prompt_names, prompt_contents):
        saved_ids.append(db_manager.save_prompt(name, content))
    
    # Retrieve all prompts
    prompts = db_manager.list_prompts()
    
    # Verify prompts
    assert len(prompts) >= 3
    
    # Check if saved prompts exist in the list
    saved_prompts = [p for p in prompts if p['id'] in saved_ids]
    assert len(saved_prompts) == 3
    
    # Verify prompt details
    for prompt, name, content in zip(saved_prompts, prompt_names, prompt_contents):
        assert prompt['prompt_name'] == name
        assert prompt['content'] == content

def test_delete_prompt(db_manager):
    """Test deleting a prompt"""
    # Save a prompt
    prompt_name = "Prompt to Delete"
    prompt_content = "This prompt will be deleted"
    prompt_id = db_manager.save_prompt(prompt_name, prompt_content)
    
    # Delete the prompt
    db_manager.delete_prompt(prompt_id)
    
    # Try to retrieve the deleted prompt
    deleted_prompt = db_manager.get_prompt(prompt_id)
    
    # Verify the prompt is deleted
    assert deleted_prompt is None

def test_nonexistent_prompt(db_manager):
    """Test retrieving a non-existent prompt"""
    # Try to retrieve a prompt with an invalid ID
    non_existent_prompt = db_manager.get_prompt(99999)
    
    # Verify no prompt is returned
    assert non_existent_prompt is None
