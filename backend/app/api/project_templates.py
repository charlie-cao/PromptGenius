from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.project import Project
from ..models.project_step import ProjectStep
from ..models.project_prompt import ProjectPrompt
from ..schemas.project import ProjectResponse
from ..utils.auth import get_current_user

router = APIRouter()

@router.post("/{project_id}/save-as-template", response_model=ProjectResponse)
async def save_as_template(
    project_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """将项目保存为模板"""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # 创建模板
    template = Project(
        name=f"{project.name} (Template)",
        description=project.description,
        tech_stack=project.tech_stack,
        is_template=True,
        user_id=current_user.id
    )
    db.add(template)
    db.flush()
    
    # 复制步骤
    for step in project.steps:
        new_step = ProjectStep(
            project_id=template.id,
            title=step.title,
            description=step.description,
            order=step.order,
            expected_output=step.expected_output
        )
        db.add(new_step)
        db.flush()
        
        # 复制提示词
        for prompt in step.prompts:
            new_prompt = ProjectPrompt(
                project_id=template.id,
                step_id=new_step.id,
                title=prompt.title,
                content=prompt.content,
                variables=prompt.variables,
                version=1,
                is_template=True
            )
            db.add(new_prompt)
    
    db.commit()
    db.refresh(template)
    return template

@router.get("/templates", response_model=List[ProjectResponse])
async def get_templates(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取项目模板列表"""
    templates = db.query(Project).filter(
        Project.user_id == current_user.id,
        Project.is_template == True
    ).all()
    return templates

@router.post("/templates/{template_id}/create", response_model=ProjectResponse)
async def create_from_template(
    template_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """从模板创建新项目"""
    template = db.query(Project).filter(
        Project.id == template_id,
        Project.user_id == current_user.id,
        Project.is_template == True
    ).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # 创建新项目
    project = Project(
        name=template.name.replace(" (Template)", ""),
        description=template.description,
        tech_stack=template.tech_stack,
        user_id=current_user.id
    )
    db.add(project)
    db.flush()
    
    # 复制步骤和提示词
    for step in template.steps:
        new_step = ProjectStep(
            project_id=project.id,
            title=step.title,
            description=step.description,
            order=step.order,
            expected_output=step.expected_output
        )
        db.add(new_step)
        db.flush()
        
        for prompt in step.prompts:
            new_prompt = ProjectPrompt(
                project_id=project.id,
                step_id=new_step.id,
                title=prompt.title,
                content=prompt.content,
                variables=prompt.variables,
                version=1
            )
            db.add(new_prompt)
    
    db.commit()
    db.refresh(project)
    return project 