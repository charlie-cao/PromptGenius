from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Enum, Boolean
from sqlalchemy.orm import relationship
from ..database import Base
import datetime
import enum

class ProjectStatus(str, enum.Enum):
    PLANNING = "planning"      # 规划中
    IN_PROGRESS = "progress"   # 进行中
    COMPLETED = "completed"    # 已完成
    ARCHIVED = "archived"      # 已归档

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    tech_stack = Column(JSON)  # 技术栈配置
    status = Column(String, default=ProjectStatus.PLANNING)
    is_template = Column(Boolean, default=False)  # 添加这个字段
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # 关联
    user = relationship("User", back_populates="projects")
    steps = relationship("ProjectStep", back_populates="project", cascade="all, delete-orphan")
    prompts = relationship("ProjectPrompt", back_populates="project", cascade="all, delete-orphan") 