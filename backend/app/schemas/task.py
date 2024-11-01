from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from enum import Enum

class TaskStatus(str, Enum):
    ALL = "all"
    COMPLETED = "completed"
    PENDING = "pending"

class TaskOrderBy(str, Enum):
    CREATED_ASC = "created_asc"
    CREATED_DESC = "created_desc"
    TITLE_ASC = "title_asc"
    TITLE_DESC = "title_desc"

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    title: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class TaskList(BaseModel):
    total: int
    items: List[TaskResponse]