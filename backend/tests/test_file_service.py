import pytest
import os
import json
from src.services import file_service

def test_read_art_file():
    """Test reading art styles file"""
    art_styles = file_service.read_art_file()
    
    assert isinstance(art_styles, list)
    assert len(art_styles) > 0
    
    # Check structure of art styles
    for style in art_styles:
        assert 'id' in style
        assert 'name' in style
        assert 'styleType' in style

def test_clear_image_folders():
    """Test clearing image folders"""
    # Create some test files in output and preview folders
    output_path = file_service.output_path
    preview_path = file_service.preview_path
    
    os.makedirs(output_path, exist_ok=True)
    os.makedirs(preview_path, exist_ok=True)
    
    # Create test files
    test_files = [
        os.path.join(output_path, 'test1.png'),
        os.path.join(output_path, 'test2.png'),
        os.path.join(preview_path, 'preview1.png')
    ]
    
    for file_path in test_files:
        with open(file_path, 'w') as f:
            f.write('test content')
    
    # Clear folders
    file_service.clear_image_folders()
    
    # Check if folders are empty
    assert len(os.listdir(output_path)) == 0
    assert len(os.listdir(preview_path)) == 0

def test_art_styles_file_exists():
    """Verify art styles file exists and is readable"""
    art_styles_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'art_styles.json')
    
    assert os.path.exists(art_styles_path)
    assert os.path.isfile(art_styles_path)
    
    # Try to parse the JSON
    try:
        with open(art_styles_path, 'r') as f:
            art_styles = json.load(f)
        
        assert isinstance(art_styles, list)
        assert len(art_styles) > 0
    except (json.JSONDecodeError, IOError) as e:
        pytest.fail(f"Error reading art styles file: {str(e)}")
