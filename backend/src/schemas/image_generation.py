
from typing import List
from pydantic import BaseModel

class GeneratedImage(BaseModel):
    filename: str
    data: str

class ImageGenerationResponse(BaseModel):
    images: List[GeneratedImage]