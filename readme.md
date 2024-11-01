# 🌟 PromptGenius | 提示工程师的魔法工坊

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8+-green.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)

PromptGenius 是一个专为提示词工程师打造的全栈开发平台，它将提示词工程的开发流程标准化，让复杂的 AI 提示词开发变得简单而优雅。

## ✨ 核心特性

### 🎯 项目管理
- 项目全生命周期管理
- 技术栈可视化
- 项目状态追踪
- 项目模板复用

### 🔄 步骤追踪
- 可视化开发流程
- 步骤拖拽排序
- 进度实时监控
- 预期输出管理

### 📝 提示词版本控制
- 提示词版本管理
- 变量模板系统
- AI 响应追踪
- 提示词性能分析

### 🛠 工具集成
- AI 工具库管理
- 工具分类系统
- 使用数据统计
- 快速访问链接

### 📊 数据分析
- 项目进度分析
- 提示词效果评估
- 工具使用统计
- 性能优化建议

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Node.js 18+
- SQLite3

### 后端安装
```bash
# 克隆仓库
git clone https://github.com/yourusername/promptgenius.git
cd promptgenius

# 创建虚拟环境
python -m venv backend/venv

# 激活虚拟环境
# Windows
backend\venv\Scripts\activate
# Linux/Mac
source backend/venv/bin/activate

# 安装依赖
cd backend
pip install -r requirements.txt

# 启动后端服务
cd app
uvicorn main:app --reload
```

### 前端安装
```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## 🎨 系统架构

### 后端技术栈
- FastAPI - 高性能 API 框架
- SQLAlchemy - ORM 框架
- Pydantic - 数据验证
- JWT - 身份认证

### 前端技术栈
- Next.js 14 - React 框架
- TypeScript - 类型安全
- Tailwind CSS - 样式框架
- SWR - 数据请求

## 📚 使用指南

1. **项目创建**
   - 创建新项目
   - 选择技术栈
   - 设置项目状态
   - 导入项目模板

2. **步骤管理**
   - 添加开发步骤
   - 设置预期输出
   - 记录实际结果
   - 调整步骤顺序

3. **提示词开发**
   - 编写提示词
   - 设置变量
   - 测试响应
   - 版本管理

4. **工具管理**
   - 添加 AI 工具
   - 分类管理
   - 快速访问
   - 使用统计

## 🤝 贡献指南

欢迎提交 Pull Request 或创建 Issue！

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/promptgenius&type=Date)](https://star-history.com/#yourusername/promptgenius&Date)

## 📧 联系我们

- 作者：[Your Name]
- 邮箱：[your.email@example.com]
- 网站：[https://promptgenius.dev](https://promptgenius.dev)

---

<p align="center">用 ❤️ 打造</p>
```

```markdown:readme.md
# 文件目录结构建议

## 项目目录结构

```
/project-root
│
├── /frontend                  # 前端代码
│   ├── /public                # 静态文件
│   ├── /src                   # 源代码
│   │   ├── /components        # 组件
│   │   ├── /pages             # 页面
│   │   ├── /styles            # 样式文件
│   │   ├── /hooks             # 自定义 Hooks
│   │   ├── /context           # 状态管理
│   │   └── /utils             # 工具函数
│   ├── package.json           # 前端依赖
│   └── next.config.js         # Next.js 配置
│
├── /backend                   # 后端代码
│   ├── /app                   # FastAPI 应用
│   │   ├── /api               # API 路由
│   │   ├── /models            # 数据库模型
│   │   ├── /schemas           # 数据验证模式
│   │   ├── /services          # 业务逻辑
│   │   └── /utils             # 工具函数
│   ├── requirements.txt       # 后端依赖
│   └── main.py                # FastAPI 启动文件
│
├── /docs                      # 文档
│   ├── architecture.md        # 架构设计
│   ├── api_reference.md       # API 参考
│   └── user_guide.md          # 用户指南
│
└── README.md                  # 项目说明文件
```

## 目录结构说明

- **/frontend**: 存放前端代码，使用 Next.js 框架。
  - **/public**: 存放静态资源，如图片和字体。
  - **/src**: 源代码目录，包含组件、页面、样式等。
  
- **/backend**: 存放后端代码，使用 FastAPI 框架。
  - **/app**: FastAPI 应用的主要逻辑，包括 API 路由和数据库模型。
  
- **/docs**: 存放项目文档，便于团队成员和用户查阅。

- **README.md**: 项目的说明文件，包含项目概述、安装和使用说明。

这种结构可以帮助你清晰地组织代码和文档，便于后期的维护和扩展。希望这个建议对你有帮助！ 
```

npx create-next-app@latest frontend  fast

# FastAPI 没有官方的脚手架工具,但可以使用以下命令快速创建项目结构:

mkdir backend
cd backend
python -m venv venv  # 创建虚拟环境
source venv/bin/activate  # Linux/Mac 激活虚拟环境
# 或 .\venv\Scripts\activate  # Windows 激活虚拟环境

pip install fastapi uvicorn
pip install python-dotenv sqlalchemy  # 常用依赖

# 创建基本目录结构
mkdir app
cd app
mkdir api models schemas services utils
touch __init__.py main.py

# 保存依赖
pip freeze > requirements.txt
