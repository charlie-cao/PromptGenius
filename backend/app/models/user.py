from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from ..database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # 添加任务关系
    tasks = relationship("Task", back_populates="user")
    
    # 添加笔记关系
    notes = relationship("Note", back_populates="user")
    
    # 添加工具关系
    tools = relationship("Tool", back_populates="user")
    
    # 添加项目关系
    projects = relationship("Project", back_populates="user")