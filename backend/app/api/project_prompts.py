from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.project_prompt import ProjectPrompt
from ..schemas.project_prompt import PromptCreate, PromptUpdate, PromptResponse, PromptList
from ..utils.auth import get_current_user
from ..models.project_step import ProjectStep
from ..models.project import Project
from pydantic import BaseModel

router = APIRouter()

# 添加重排序请求的模型
class PromptOrderItem(BaseModel):
    id: int
    order: int

class PromptReorderRequest(BaseModel):
    step_id: int
    prompts: List[PromptOrderItem]

@router.post("/", response_model=PromptResponse)
async def create_prompt(
    prompt: PromptCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建新提示词"""
    # 验证项目所有权
    project = db.query(Project).filter(
        Project.id == prompt.project_id,
        Project.user_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # 如果提供了步骤ID，验证步骤存在性
    if prompt.step_id:
        step = db.query(ProjectStep).filter(
            ProjectStep.id == prompt.step_id,
            ProjectStep.project_id == prompt.project_id
        ).first()
        if not step:
            raise HTTPException(status_code=404, detail="Step not found")
    
    # 获取当前最大顺序号
    max_order = db.query(ProjectPrompt).filter(
        ProjectPrompt.step_id == prompt.step_id
    ).count()
    
    # 创建新提示词，移除可能重复的字段
    prompt_data = prompt.model_dump()
    prompt_data.pop('version', None)  # 移除 version 字段
    prompt_data.pop('order', None)    # 移除 order 字段
    
    # 创建新提示词
    db_prompt = ProjectPrompt(
        **prompt_data,
        version=1,           # 新提示词版本从1开始
        order=max_order + 1  # 设置顺序号
    )
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

@router.get("/step/{step_id}", response_model=PromptList)
async def get_step_prompts(
    step_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取步骤的所有提示词"""
    # 验证步骤所属项目的所有权
    step = db.query(ProjectStep).join(Project).filter(
        ProjectStep.id == step_id,
        Project.user_id == current_user.id
    ).first()
    
    if not step:
        raise HTTPException(status_code=404, detail="Step not found")
    
    prompts = db.query(ProjectPrompt).filter(
        ProjectPrompt.step_id == step_id
    ).order_by(ProjectPrompt.order, ProjectPrompt.version.desc()).all()  # 先按顺序，再按版本排序
    
    return PromptList(items=prompts)

@router.put("/{prompt_id}", response_model=PromptResponse)
async def update_prompt(
    prompt_id: int,
    prompt_update: PromptUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新提示词"""
    # 验证提示词所属项目的所有权
    prompt = db.query(ProjectPrompt).join(Project).filter(
        ProjectPrompt.id == prompt_id,
        Project.user_id == current_user.id
    ).first()
    
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # 更新提示词
    for field, value in prompt_update.model_dump(exclude_unset=True).items():
        setattr(prompt, field, value)
    
    db.commit()
    db.refresh(prompt)
    return prompt

@router.delete("/{prompt_id}")
async def delete_prompt(
    prompt_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除提示词"""
    prompt = db.query(ProjectPrompt).join(Project).filter(
        ProjectPrompt.id == prompt_id,
        Project.user_id == current_user.id
    ).first()
    
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    db.delete(prompt)
    db.commit()
    return {"message": "Prompt deleted successfully"}

@router.post("/{prompt_id}/versions", response_model=PromptResponse)
async def create_prompt_version(
    prompt_id: int,
    prompt_update: PromptUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建提示词新版本"""
    original = db.query(ProjectPrompt).join(Project).filter(
        ProjectPrompt.id == prompt_id,
        Project.user_id == current_user.id
    ).first()
    
    if not original:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # 获取当前最大版本号
    max_version = db.query(ProjectPrompt).filter(
        ProjectPrompt.project_id == original.project_id,
        ProjectPrompt.step_id == original.step_id
    ).count()
    
    # 创建新版本
    new_version = ProjectPrompt(
        title=prompt_update.title or original.title,
        content=prompt_update.content or original.content,
        variables=prompt_update.variables or original.variables,
        project_id=original.project_id,
        step_id=original.step_id,
        version=max_version + 1
    )
    
    db.add(new_version)
    db.commit()
    db.refresh(new_version)
    return new_version

@router.get("/{prompt_id}/versions", response_model=List[PromptResponse])
async def get_prompt_versions(
    prompt_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取提示词的所有版本"""
    prompt = db.query(ProjectPrompt).join(Project).filter(
        ProjectPrompt.id == prompt_id,
        Project.user_id == current_user.id
    ).first()
    
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    versions = db.query(ProjectPrompt).filter(
        ProjectPrompt.project_id == prompt.project_id,
        ProjectPrompt.step_id == prompt.step_id
    ).order_by(ProjectPrompt.version.desc()).all()
    
    return versions

@router.put("/reorder", response_model=PromptList)
async def reorder_prompts(
    reorder_data: PromptReorderRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """重新排序提示词"""
    # 验证步骤所属项目的所有权
    step = db.query(ProjectStep).join(Project).filter(
        ProjectStep.id == reorder_data.step_id,
        Project.user_id == current_user.id
    ).first()
    
    if not step:
        raise HTTPException(status_code=404, detail="Step not found")
    
    # 获取所有需要更新的提示词
    prompt_ids = [prompt.id for prompt in reorder_data.prompts]
    prompts = db.query(ProjectPrompt).filter(
        ProjectPrompt.id.in_(prompt_ids),
        ProjectPrompt.step_id == reorder_data.step_id
    ).all()
    
    # 创建 id 到提示词的映射
    prompts_map = {prompt.id: prompt for prompt in prompts}
    
    # 更新提示词顺序
    for prompt_order in reorder_data.prompts:
        if prompt_order.id in prompts_map:
            prompts_map[prompt_order.id].order = prompt_order.order
    
    db.commit()
    
    # 返回更新后的提示词列表
    updated_prompts = db.query(ProjectPrompt).filter(
        ProjectPrompt.step_id == reorder_data.step_id
    ).order_by(ProjectPrompt.order).all()
    
    return PromptList(items=updated_prompts)