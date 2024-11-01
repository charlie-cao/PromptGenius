from sqlalchemy.orm import Session
from .models.tool import Tool
from .schemas.tool import ToolCategory
from .migrations.initial_tools import create_initial_tools
from .migrations.initial_projects import create_initial_project
from .models.project import Project

def init_tools(db: Session, user_id: int):
    """初始化工具数据"""
    # 检查是否已有工具数据
    existing_tools = db.query(Tool).filter(Tool.user_id == user_id).count()
    if existing_tools > 0:
        return {"message": "Tools already initialized"}
    
    # 创建初始工具数据
    create_initial_tools(db, user_id)
    return {"message": "Tools initialized successfully"}

def init_project(db: Session, user_id: int):
    """初始化示例项目"""
    # 检查是否已有项目
    existing_project = db.query(Project).filter(
        Project.user_id == user_id,
        Project.name == "提示词工程师助手"
    ).first()
    
    if existing_project:
        return {"message": "Project already exists"}
    
    # 创建示例项目
    create_initial_project(db, user_id)
    return {"message": "Project initialized successfully"} 