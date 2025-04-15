from pydantic import BaseModel


class PromptGenerationResponse(BaseModel):
    generated_prompt: str


class KeywordGenerationResponse(BaseModel):
    keywords: list
