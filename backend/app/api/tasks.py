from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from ..database import get_db
from ..models.task import Task
from ..schemas.task import (
    TaskCreate, TaskUpdate, TaskResponse, TaskList,
    TaskStatus, TaskOrderBy
)
from ..utils.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=TaskResponse)
async def create_task(
    task: TaskCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建新任务"""
    db_task = Task(**task.model_dump(), user_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/", response_model=TaskList)
async def get_tasks(
    search: Optional[str] = None,
    status: TaskStatus = TaskStatus.ALL,
    order_by: TaskOrderBy = TaskOrderBy.CREATED_DESC,
    page: int = Query(1, gt=0),
    page_size: int = Query(10, gt=0, le=100),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取任务列表，支持搜索、过滤和排序"""
    query = db.query(Task).filter(Task.user_id == current_user.id)
    
    # 搜索
    if search:
        query = query.filter(
            or_(
                Task.title.ilike(f"%{search}%"),
                Task.description.ilike(f"%{search}%")
            )
        )
    
    # 状态过滤
    if status == TaskStatus.COMPLETED:
        query = query.filter(Task.completed == True)
    elif status == TaskStatus.PENDING:
        query = query.filter(Task.completed == False)
    
    # 排序
    if order_by == TaskOrderBy.CREATED_ASC:
        query = query.order_by(Task.created_at.asc())
    elif order_by == TaskOrderBy.CREATED_DESC:
        query = query.order_by(Task.created_at.desc())
    elif order_by == TaskOrderBy.TITLE_ASC:
        query = query.order_by(Task.title.asc())
    elif order_by == TaskOrderBy.TITLE_DESC:
        query = query.order_by(Task.title.desc())
    
    # 计算总数
    total = query.count()
    
    # 分页
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    return {
        "total": total,
        "items": query.all()
    }

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取特定任务"""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新任务"""
    db_task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # 只更新提供的字段
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除任务"""
    db_task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"} 