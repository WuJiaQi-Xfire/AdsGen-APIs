# Backend Test Suite

### Run All Tests
```bash
pytest tests/
```

### Run Specific Test Files
```bash
# Run database tests
pytest tests/test_database.py

# Run service tests
pytest tests/test_gpt_service.py
pytest tests/test_comfy_service.py
pytest tests/test_file_service.py

# Run endpoint tests
pytest tests/test_full_endpoints.py
```

### Test Coverage Details

#### Database Tests (`test_database.py`)
- Prompt creation and retrieval
- Listing prompts
- Deleting prompts
- Handling non-existent prompts

#### GPT Service Tests (`test_gpt_service.py`)
- Prompt generation
- Keyword extraction
- Error handling for invalid inputs

#### Comfy Service Tests (`test_comfy_service.py`)
- Image generation workflows
- Lora style image generation
- Verifying image paths and generation

#### File Service Tests (`test_file_service.py`)
- Reading art styles
- Clearing image folders
- Validating art styles file

#### Full Endpoint Tests (`test_full_endpoints.py`)
- Generate prompt endpoint
- Extract keywords endpoint
- Get styles endpoint
- Image generation endpoint

## Troubleshooting

- Ensure all dependencies are installed
- Check that you're in the correct directory
- Verify Python and pip versions
- For any connection-related tests, ensure ComfyUI and other services are running

## Notes

- Tests use temporary databases to avoid affecting production data
- Some tests may require active services to be running
- Test coverage is comprehensive but not absolute

## Contributing

- Add new tests for any new features or services
- Maintain existing test structure
- Ensure all tests pass before submitting changes
