from pydantic import BaseModel
from typing import List

class TextFileResponse(BaseModel):
    text_content: str

class ImageUploadResponse(BaseModel):
    image_base64: str
    format: str

class PromptRequest(BaseModel):
    categories: List[str]
    project_style: str

class PromptResponse(BaseModel):
    prompts: List[str]

class ImageGenerationRequest(BaseModel):
    prompt: str
    num_images: int

class ImageGenerationResponse(BaseModel):
    images: List[str]