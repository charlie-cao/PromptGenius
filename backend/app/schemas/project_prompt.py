from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List, Dict

class PromptBase(BaseModel):
    title: str
    content: str
    variables: Optional[Dict[str, str]] = None  # 提示词变量，例如: {"project_name": "MyApp", "language": "Python"}
    version: int = 1
    order: Optional[int] = None   # 添加 order 字段
    is_template: bool = False

class PromptCreate(PromptBase):
    project_id: int
    step_id: Optional[int] = None
    # 移除 order 字段，它将在创建时自动设置
    class Config:
        exclude = {'order'}  # 排除 order 字段

class PromptUpdate(PromptBase):
    title: Optional[str] = None
    content: Optional[str] = None
    variables: Optional[Dict[str, str]] = None
    version: Optional[int] = None
    order: Optional[int] = None
    is_template: Optional[bool] = None

class PromptResponse(PromptBase):
    id: int
    project_id: int
    step_id: Optional[int]
    response: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class PromptList(BaseModel):
    items: List[PromptResponse]
    
    model_config = ConfigDict(from_attributes=True)

# 添加重排序请求的模型
class PromptOrderItem(BaseModel):
    id: int
    order: int

class PromptReorderRequest(BaseModel):
    step_id: int
    prompts: List[PromptOrderItem]