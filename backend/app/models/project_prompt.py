from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from ..database import Base
import datetime

class ProjectPrompt(Base):
    __tablename__ = "project_prompts"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    step_id = Column(Integer, ForeignKey("project_steps.id"))
    title = Column(String, index=True)
    content = Column(Text)        # 提示词内容
    response = Column(Text)       # AI 响应
    variables = Column(JSON)      # 提示词变量
    version = Column(Integer)     # 提示词版本
    order = Column(Integer)       # 提示词顺序
    is_template = Column(Boolean, default=False)  # 是否是模板
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # 关联
    project = relationship("Project", back_populates="prompts")
    step = relationship("ProjectStep", back_populates="prompts")