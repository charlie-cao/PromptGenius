from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from ..database import Base
import datetime

class ProjectStep(Base):
    __tablename__ = "project_steps"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    title = Column(String, index=True)
    description = Column(Text)
    order = Column(Integer)  # 步骤顺序
    is_completed = Column(Boolean, default=False)
    expected_output = Column(Text)  # 预期输出
    actual_output = Column(Text)    # 实际输出
    notes = Column(Text)            # 步骤笔记
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # 关联
    project = relationship("Project", back_populates="steps")
    prompts = relationship("ProjectPrompt", back_populates="step", cascade="all, delete-orphan")