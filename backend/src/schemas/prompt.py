from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# 基础Prompt模型
class PromptBase(BaseModel):
    prompt_name: str
    content: str

# 创建Prompt时使用的模型
class PromptCreate(PromptBase):
    pass

# 更新Prompt时使用的模型
class PromptUpdate(BaseModel):
    prompt_name: Optional[str] = None
    content: Optional[str] = None

# 数据库中的Prompt模型
class Prompt(PromptBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
