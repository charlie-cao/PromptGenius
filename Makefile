# 设置 shell
SHELL := cmd.exe
.PHONY: frontend backend clean run-frontend run-backend help

# 默认目标
.DEFAULT_GOAL := help

# 帮助信息
help:
	@echo off
	@chcp 65001 >nul
	@echo 使用方法:
	@echo   make frontend     - 创建前端项目
	@echo   make backend      - 创建后端项目
	@echo   make clean        - 清理项目
	@echo   make run-frontend - 运行前端项目
	@echo   make run-backend  - 运行后端项目

# 创建前端项目
frontend:
	@echo off
	@chcp 65001 >nul
	@echo 创建前端项目...
	npx create-next-app@latest frontend 

# 创建后端项目
backend:
	@echo off
	@chcp 65001 >nul
	@echo 创建后端项目...
	mkdir backend\app\api backend\app\models backend\app\schemas backend\app\services backend\app\utils 2>nul
	python -m venv backend\venv
	backend\venv\Scripts\pip install fastapi uvicorn python-dotenv sqlalchemy
	backend\venv\Scripts\pip freeze > backend\requirements.txt
	@echo from fastapi import FastAPI> backend\app\main.py
	@echo from fastapi.middleware.cors import CORSMiddleware>> backend\app\main.py
	@echo.>> backend\app\main.py
	@echo app = FastAPI()>> backend\app\main.py
	@echo.>> backend\app\main.py
	@echo app.add_middleware(>> backend\app\main.py
	@echo     CORSMiddleware,>> backend\app\main.py
	@echo     allow_origins=["http://localhost:3000"],>> backend\app\main.py
	@echo     allow_credentials=True,>> backend\app\main.py
	@echo     allow_methods=["*"],>> backend\app\main.py
	@echo     allow_headers=["*"],>> backend\app\main.py
	@echo )>> backend\app\main.py
	@echo.>> backend\app\main.py
	@echo @app.get("/")>> backend\app\main.py
	@echo async def root():>> backend\app\main.py
	@echo     return {"message": "Welcome to FastAPI"}>> backend\app\main.py
	type nul > backend\app\__init__.py

# 清理项目
clean:
	@echo off
	@chcp 65001 >nul
	@echo 清理项目...
	@if exist frontend rmdir /s /q frontend
	@if exist backend rmdir /s /q backend
	@echo 清理完成！

# 运行前端项目
run-frontend:
	@echo off
	@chcp 65001 >nul
	@if not exist frontend ( echo 错误：前端目录不存在，请先创建项目 & exit /b 1 )
	@echo 启动前端项目...
	@cmd /c "cd frontend && start cmd /k npm run dev"
	@echo 前端项目已启动！

# 运行后端项目
run-backend:
	@echo off
	@chcp 65001 >nul
	@if not exist backend ( echo 错误：后端目录不存在，请先创建项目 & exit /b 1 )
	@echo 启动后端项目...
	@cmd /c "cd backend && start cmd /k "".\venv\Scripts\activate && cd app && uvicorn main:app --reload"""
	@echo 后端项目已启动！