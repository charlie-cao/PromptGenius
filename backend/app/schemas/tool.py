from pydantic import BaseModel, ConfigDict, HttpUrl
from datetime import datetime
from typing import Optional, List
from enum import Enum

class ToolCategory(str, Enum):
    AI_CHAT = "ai_chat"          # AI 对话和助手
    PROMPT = "prompt"            # 提示词工具
    IMAGE = "image"              # 图像生成
    VIDEO = "video"              # 视频生成
    AUDIO = "audio"              # 音频处理
    CODE = "code"                # 代码开发
    WRITING = "writing"          # 写作助手
    RESEARCH = "research"        # 研究和分析
    PRODUCTIVITY = "productivity" # 生产力工具
    EDUCATION = "education"      # 教育工具
    BUSINESS = "business"        # 商业工具
    OTHER = "other"              # 其他

class ToolBase(BaseModel):
    name: str
    description: str
    url: HttpUrl
    icon: Optional[str] = None
    category: ToolCategory = ToolCategory.OTHER

class ToolCreate(ToolBase):
    pass

class ToolUpdate(ToolBase):
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[HttpUrl] = None
    icon: Optional[str] = None
    category: Optional[ToolCategory] = None

class ToolResponse(ToolBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ToolList(BaseModel):
    total: int
    items: List[ToolResponse]
    
    model_config = ConfigDict(from_attributes=True)