from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.project import Project
from ..models.project_step import ProjectStep
from ..schemas.project_step import StepCreate, StepUpdate, StepResponse, StepList
from ..utils.auth import get_current_user
from pydantic import BaseModel

router = APIRouter()

class StepOrderItem(BaseModel):
    id: int
    order: int

class StepReorderRequest(BaseModel):
    project_id: int
    steps: List[StepOrderItem]

@router.post("/", response_model=StepResponse)
async def create_step(
    step: StepCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建新步骤"""
    # 验证项目所有权
    project = db.query(Project).filter(
        Project.id == step.project_id,
        Project.user_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db_step = ProjectStep(**step.model_dump())
    db.add(db_step)
    db.commit()
    db.refresh(db_step)
    return db_step

@router.get("/project/{project_id}", response_model=StepList)
async def get_project_steps(
    project_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取项目的所有步骤"""
    # 验证项目所有权
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    steps = db.query(ProjectStep).filter(
        ProjectStep.project_id == project_id
    ).order_by(ProjectStep.order).all()
    
    return {"items": steps}

@router.put("/reorder", response_model=StepList)
async def reorder_steps(
    reorder_data: StepReorderRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """重新排序步骤"""
    # 验证项目所有权
    project = db.query(Project).filter(
        Project.id == reorder_data.project_id,
        Project.user_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # 获取所有需要更新的步骤
    step_ids = [step.id for step in reorder_data.steps]
    steps = db.query(ProjectStep).filter(
        ProjectStep.id.in_(step_ids),
        ProjectStep.project_id == reorder_data.project_id
    ).all()
    
    # 创建 id 到步骤的映射
    steps_map = {step.id: step for step in steps}
    
    # 更新步骤顺序
    for step_order in reorder_data.steps:
        if step_order.id in steps_map:
            steps_map[step_order.id].order = step_order.order
    
    db.commit()
    
    # 返回更新后的步骤列表
    updated_steps = db.query(ProjectStep).filter(
        ProjectStep.project_id == reorder_data.project_id
    ).order_by(ProjectStep.order).all()
    
    return StepList(items=updated_steps)

@router.put("/{step_id}", response_model=StepResponse)
async def update_step(
    step_id: int,
    step_update: StepUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新步骤"""
    step = db.query(ProjectStep).join(Project).filter(
        ProjectStep.id == step_id,
        Project.user_id == current_user.id
    ).first()
    if not step:
        raise HTTPException(status_code=404, detail="Step not found")
    
    for field, value in step_update.model_dump(exclude_unset=True).items():
        setattr(step, field, value)
    
    db.commit()
    db.refresh(step)
    return step

@router.delete("/{step_id}")
async def delete_step(
    step_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除步骤"""
    step = db.query(ProjectStep).join(Project).filter(
        ProjectStep.id == step_id,
        Project.user_id == current_user.id
    ).first()
    if not step:
        raise HTTPException(status_code=404, detail="Step not found")
    
    # 更新后续步骤的顺序
    subsequent_steps = db.query(ProjectStep).filter(
        ProjectStep.project_id == step.project_id,
        ProjectStep.order > step.order
    ).all()
    for subsequent_step in subsequent_steps:
        subsequent_step.order -= 1
    
    db.delete(step)
    db.commit()
    return {"message": "Step deleted successfully"} 