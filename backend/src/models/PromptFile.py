from pydantic import BaseModel

class PromptFile(BaseModel):
      id: str
      name: str
      content: str
      selected: bool
