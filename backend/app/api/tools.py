from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from ..database import get_db
from ..models.tool import Tool
from ..schemas.tool import ToolCreate, ToolUpdate, ToolResponse, ToolCategory, ToolList
from ..utils.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=ToolResponse)
async def create_tool(
    tool: ToolCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建新工具"""
    db_tool = Tool(**tool.model_dump(), user_id=current_user.id)
    db.add(db_tool)
    db.commit()
    db.refresh(db_tool)
    return db_tool

@router.get("/", response_model=ToolList)
async def get_tools(
    category: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(1, gt=0),
    page_size: int = Query(12, gt=0, le=100),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取工具列表，支持分页、搜索和分类过滤"""
    query = db.query(Tool).filter(Tool.user_id == current_user.id)
    
    # 分类过滤
    if category and category != 'all':
        query = query.filter(Tool.category == category)
    
    # 搜索
    if search:
        query = query.filter(
            or_(
                Tool.name.ilike(f"%{search}%"),
                Tool.description.ilike(f"%{search}%")
            )
        )
    
    # 计算总数
    total = query.count()
    
    # 分页
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return ToolList(total=total, items=items)

@router.get("/{tool_id}", response_model=ToolResponse)
async def get_tool(
    tool_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取特定工具"""
    tool = db.query(Tool).filter(
        Tool.id == tool_id,
        Tool.user_id == current_user.id
    ).first()
    if tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    return tool

@router.put("/{tool_id}", response_model=ToolResponse)
async def update_tool(
    tool_id: int,
    tool_update: ToolUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新工具"""
    db_tool = db.query(Tool).filter(
        Tool.id == tool_id,
        Tool.user_id == current_user.id
    ).first()
    if db_tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    
    update_data = tool_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_tool, field, value)
    
    db.commit()
    db.refresh(db_tool)
    return db_tool

@router.delete("/{tool_id}")
async def delete_tool(
    tool_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除工具"""
    db_tool = db.query(Tool).filter(
        Tool.id == tool_id,
        Tool.user_id == current_user.id
    ).first()
    if db_tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    
    db.delete(db_tool)
    db.commit()
    return {"message": "Tool deleted successfully"}

@router.post("/init", response_model=dict)
async def initialize_tools(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """初始化工具数据"""
    from ..commands import init_tools
    return init_tools(db, current_user.id) 