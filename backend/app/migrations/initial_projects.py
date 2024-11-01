from sqlalchemy.orm import Session
from ..models.project import Project, ProjectStatus
from ..models.project_step import ProjectStep
from ..models.project_prompt import ProjectPrompt

def create_initial_project(db: Session, user_id: int):
    """创建初始项目 - 提示词工程师助手"""
    
    # 创建项目
    project = Project(
        name="提示词工程师助手",
        description="一个帮助管理和优化提示词工程开发流程的工具。支持项目管理、步骤追踪、提示词版本控制等功能。",
        tech_stack={
            "frontend": ["Next.js", "TypeScript", "Tailwind CSS"],
            "backend": ["Python", "FastAPI", "SQLAlchemy"],
            "database": ["SQLite"],
            "devops": ["Git"]
        },
        status=ProjectStatus.COMPLETED,
        user_id=user_id
    )
    db.add(project)
    db.flush()

    # 创建步骤
    steps = [
        {
            "title": "项目设计",
            "description": "设计项目的数据模型和基本功能",
            "order": 1,
            "is_completed": True,
            "expected_output": "完整的数据模型设计和API规划",
            "prompts": [
                {
                    "title": "数据模型设计",
                    "content": "我需要设计一个提示词工程开发流程管理系统，包括以下功能：\n1. 项目管理\n2. 步骤追踪\n3. 提示词版本控制\n请帮我设计合适的数据模型。",
                    "response": "让我们设计项目模型：\n\n1. Project模型：\n- id, name, description\n- tech_stack (JSON)\n- status (enum)\n- user_id (外键)\n\n2. ProjectStep模型：\n- id, project_id\n- title, description\n- order, is_completed\n- expected_output, actual_output\n\n3. ProjectPrompt模型：\n- id, project_id, step_id\n- title, content\n- variables (JSON)\n- version\n- is_template",
                    "version": 1
                }
            ]
        },
        {
            "title": "API实现",
            "description": "实现后端API接口",
            "order": 2,
            "is_completed": True,
            "expected_output": "完整的后端API实现，包括项目、步骤和提示词的CRUD操作",
            "prompts": [
                {
                    "title": "API路由设计",
                    "content": "基于之前设计的数��模型，请帮我实现FastAPI的路由。需要包括：\n1. 项目的CRUD操作\n2. 步骤的管理和排序\n3. 提示词的版本控制\n4. 模板的管理和应用",
                    "response": "已实现所有需要的API路由：\n1. /api/projects/ - 项目管理\n2. /api/project_steps/ - 步骤管理\n3. /api/project_prompts/ - 提示词管理\n4. /api/project_templates/ - 模板管理",
                    "version": 1
                }
            ]
        },
        {
            "title": "前端实现",
            "description": "实现前端界面",
            "order": 3,
            "is_completed": True,
            "expected_output": "完整的前端界面实现，包括项目列表、详情页、步骤管理和提示词编辑器",
            "prompts": [
                {
                    "title": "页面组件设计",
                    "content": "请帮我设计Next.js的页面组件，需要包括：\n1. 项目列表页\n2. 项目详情页\n3. 步骤管理组件\n4. 提示词编辑器组件",
                    "response": "已实现所有需要的页面和组件：\n1. /projects/page.tsx - 项目列表\n2. /projects/[id]/page.tsx - 项目详情\n3. StepForm.tsx - 步骤表单\n4. PromptEditor.tsx - 提示词编辑器",
                    "version": 1
                }
            ]
        }
    ]

    for step_data in steps:
        prompts = step_data.pop('prompts')
        step = ProjectStep(project_id=project.id, **step_data)
        db.add(step)
        db.flush()

        for prompt_data in prompts:
            prompt = ProjectPrompt(
                project_id=project.id,
                step_id=step.id,
                **prompt_data
            )
            db.add(prompt)

    db.commit()
    return project 