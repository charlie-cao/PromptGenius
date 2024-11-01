from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.project import Project
from ..models.project_step import ProjectStep
from ..models.project_prompt import ProjectPrompt
from ..schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectList, ProjectStatus
from ..utils.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建新项目"""
    db_project = Project(**project.model_dump(), user_id=current_user.id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.get("/", response_model=ProjectList)
async def get_projects(
    search: Optional[str] = None,
    status: Optional[str] = None,
    page: int = Query(1, gt=0),
    page_size: int = Query(10, gt=0, le=100),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取项目列表"""
    query = db.query(Project).filter(Project.user_id == current_user.id)
    
    if search:
        query = query.filter(Project.name.ilike(f"%{search}%"))
    if status and status != 'all':
        query = query.filter(Project.status == status)
    
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return ProjectList(total=total, items=items)

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取项目详情"""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新项目"""
    db_project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    for field, value in project_update.model_dump(exclude_unset=True).items():
        setattr(db_project, field, value)
    
    db.commit()
    db.refresh(db_project)
    return db_project

@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除项目"""
    db_project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(db_project)
    db.commit()
    return {"message": "Project deleted successfully"}

@router.post("/{project_id}/duplicate", response_model=ProjectResponse)
async def duplicate_project(
    project_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """复制项目（包括步骤和提示词）"""
    # 获取原项目
    source_project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    if not source_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # 创建新项目
    new_project = Project(
        name=f"{source_project.name} (复制)",
        description=source_project.description,
        tech_stack=source_project.tech_stack,
        status=ProjectStatus.PLANNING,
        user_id=current_user.id
    )
    db.add(new_project)
    db.flush()  # 获取新项目ID
    
    # 复制步骤
    for step in source_project.steps:
        new_step = ProjectStep(
            project_id=new_project.id,
            title=step.title,
            description=step.description,
            order=step.order,
            expected_output=step.expected_output,
            actual_output=step.actual_output,
            notes=step.notes
        )
        db.add(new_step)
        db.flush()
        
        # 复制提示词
        for prompt in step.prompts:
            new_prompt = ProjectPrompt(
                project_id=new_project.id,
                step_id=new_step.id,
                title=prompt.title,
                content=prompt.content,
                variables=prompt.variables,
                version=1
            )
            db.add(new_prompt)
    
    db.commit()
    db.refresh(new_project)
    return new_project

@router.post("/{project_id}/export")
async def export_project(
    project_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """导出项目为可重放的脚本"""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # 构建项目脚本
    script = {
        "project": {
            "name": project.name,
            "description": project.description,
            "tech_stack": project.tech_stack
        },
        "steps": []
    }
    
    for step in project.steps:
        step_data = {
            "title": step.title,
            "description": step.description,
            "order": step.order,
            "expected_output": step.expected_output,
            "prompts": []
        }
        
        for prompt in step.prompts:
            step_data["prompts"].append({
                "title": prompt.title,
                "content": prompt.content,
                "variables": prompt.variables,
                "response": prompt.response
            })
        
        script["steps"].append(step_data)
    
    return script 

@router.post("/init", response_model=dict)
async def initialize_project(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """初始化示例项目"""
    from ..commands import init_project
    return init_project(db, current_user.id)