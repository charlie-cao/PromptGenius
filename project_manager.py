import os
import subprocess
import platform
from pathlib import Path
import sys
from typing import Optional

class ProjectManager:
    def __init__(self):
        self.root_dir = Path.cwd()
        self.frontend_dir = self.root_dir / 'frontend'
        self.backend_dir = self.root_dir / 'backend'
        self.app_dir = self.backend_dir / 'app'

    def _run_command(self, command: str, cwd: Optional[Path] = None):
        """运行命令并实时输出结果"""
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=cwd,
            bufsize=1,
            universal_newlines=True,
            encoding='utf-8'
        )
        
        # 实时读取输出
        while process.poll() is None:
            # 读取一行输出
            line = process.stdout.readline()
            if line:
                print(line.strip())
            
            # 读取一行错误
            error = process.stderr.readline()
            if error:
                print(f"错误: {error.strip()}")
        
        # 确保读取所有剩余输出
        stdout, stderr = process.communicate()
        if stdout:
            print(stdout.strip())
        if stderr:
            print(f"错误: {stderr.strip()}")
        
        return process.returncode

    def create_frontend(self):
        """创建前端项目"""
        print("开始创建前端项目...")
        
        if self.frontend_dir.exists():
            print("前端目录已存在，请先清理或使用其他目录")
            return
            
        # 使用最新的 create-next-app 命令行参数
        self._run_command(
            "npx create-next-app@latest frontend "
            "--typescript=false "     # 不使用 TypeScript
            "--tailwind=true "       # 使用 Tailwind CSS
            "--eslint=true "         # 使用 ESLint
            "--src-dir=true "        # 使用 src 目录
            "--app=false "           # 不使用 App Router
            "--import-alias='@/*' "  # 设置导入别名
            "--use-npm=true "        # 使用 npm
            "--no-git "              # 不初始化 git
            "--skip-instructions "    # 跳过说明
            "--default "             # 使用默认值
        )
        print("前端项目创建完成！")

    def create_backend(self):
        """创建后端项目"""
        print("开始创建后端项目...")
        
        if self.backend_dir.exists():
            print("后端目录已存在，请先清理或使用其他目录")
            return
            
        # 创建基本目录结构
        os.makedirs(self.backend_dir)
        os.chdir(self.backend_dir)
        
        # 创建虚拟环境
        print("创建虚拟环境...")
        self._run_command("python -m venv venv")
        
        # 安装依赖
        print("安装依赖...")
        activate_cmd = "source venv/bin/activate" if platform.system() != "Windows" else ".\\venv\\Scripts\\activate"
        self._run_command(f"{activate_cmd} && pip install fastapi uvicorn python-dotenv sqlalchemy")
        
        # 创建项目结构
        print("创建项目结构...")
        os.makedirs(self.app_dir)
        for dir_name in ['api', 'models', 'schemas', 'services', 'utils']:
            os.makedirs(self.app_dir / dir_name)
        
        # 创建主文件
        self._create_main_py()
        
        # 保存依赖
        self._run_command(f"{activate_cmd} && pip freeze > requirements.txt")
        
        os.chdir(self.root_dir)
        print("后端项目创建完成！")

    def _create_main_py(self):
        """创建 main.py 文件"""
        main_content = '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI"}
'''
        with open(self.app_dir / 'main.py', 'w') as f:
            f.write(main_content)
        (self.app_dir / '__init__.py').touch()

    def clean(self):
        """清理项目"""
        print("清理项目...")
        if platform.system() == "Windows":
            os.system("rmdir /s /q frontend")
            os.system("rmdir /s /q backend")
        else:
            os.system("rm -rf frontend")
            os.system("rm -rf backend")
        print("清理完成！")

    def run(self):
        """运行项目"""
        if not (self.frontend_dir.exists() and self.backend_dir.exists()):
            print("错误：前端或后端目录不存在，请先创建项目")
            return
            
        print("启动项目...")
        if platform.system() == "Windows":
            os.system("start cmd /k \"cd frontend && npm run dev\"")
            os.system("start cmd /k \"cd backend && .\\venv\\Scripts\\activate && cd app && uvicorn main:app --reload\"")
        else:
            os.system("gnome-terminal -- bash -c 'cd frontend && npm run dev'")
            os.system("gnome-terminal -- bash -c 'cd backend && source venv/bin/activate && cd app && uvicorn main:app --reload'")
        print("项目已启动！")

def main():
    manager = ProjectManager()
    
    if len(sys.argv) < 2:
        print("""
使用方法: python project_manager.py [command]
可用命令:
  frontend  - 创建前端项目
  backend   - 创建后端项目
  clean     - 清理项目
  run       - 运行项目
        """)
        sys.exit(1)
    
    command = sys.argv[1]
    
    commands = {
        'frontend': manager.create_frontend,
        'backend': manager.create_backend,
        'clean': manager.clean,
        'run': manager.run
    }
    
    if command in commands:
        commands[command]()
    else:
        print(f"未知命令: {command}")
        print("可用命令: frontend, backend, clean, run")
        sys.exit(1)

if __name__ == "__main__":
    main() 