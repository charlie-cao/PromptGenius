from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List, Dict
from enum import Enum

class ProjectStatus(str, Enum):
    PLANNING = "planning"      # 规划中
    IN_PROGRESS = "progress"   # 进行中
    COMPLETED = "completed"    # 已完成
    ARCHIVED = "archived"      # 已归档

class ProjectBase(BaseModel):
    name: str
    description: str
    tech_stack: Dict[str, List[str]]  # 例如: {"frontend": ["React", "Next.js"], "backend": ["FastAPI", "SQLAlchemy"]}
    status: ProjectStatus = ProjectStatus.PLANNING

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    name: Optional[str] = None
    description: Optional[str] = None
    tech_stack: Optional[Dict[str, List[str]]] = None
    status: Optional[ProjectStatus] = None

class ProjectResponse(ProjectBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ProjectList(BaseModel):
    total: int
    items: List[ProjectResponse]
    
    model_config = ConfigDict(from_attributes=True) 