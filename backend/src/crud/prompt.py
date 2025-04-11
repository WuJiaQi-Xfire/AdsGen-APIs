from .base import CRUDBase
from src.models.prompt import Prompt as PromptModel
from src.schemas.prompt import PromptCreate, PromptUpdate

class CRUDPrompt(CRUDBase[PromptModel, PromptCreate, PromptUpdate]):
    pass

prompt = CRUDPrompt(PromptModel)
