from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .api import auth, tasks, notes, tools, projects, project_steps, project_prompts, project_templates

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(notes.router, prefix="/api/notes", tags=["notes"])
app.include_router(tools.router, prefix="/api/tools", tags=["tools"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(project_steps.router, prefix="/api/project_steps", tags=["project_steps"])
app.include_router(project_prompts.router, prefix="/api/project_prompts", tags=["project_prompts"])
app.include_router(project_templates.router, prefix="/api/project_templates", tags=["project_templates"])

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI"}
