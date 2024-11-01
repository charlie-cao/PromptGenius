from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

class StepBase(BaseModel):
    title: str
    description: str
    order: int
    expected_output: Optional[str] = None
    actual_output: Optional[str] = None
    notes: Optional[str] = None
    is_completed: bool = False

class StepCreate(StepBase):
    project_id: int

class StepUpdate(StepBase):
    title: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None
    expected_output: Optional[str] = None
    actual_output: Optional[str] = None
    notes: Optional[str] = None
    is_completed: Optional[bool] = None

class StepResponse(StepBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class StepList(BaseModel):
    items: List[StepResponse]
    
    model_config = ConfigDict(from_attributes=True) 