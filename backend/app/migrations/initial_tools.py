from sqlalchemy.orm import Session
from ..models.tool import Tool
from ..schemas.tool import ToolCategory

def create_initial_tools(db: Session, user_id: int):
    tools = [
        # AI 对话和助手类
        {
            "name": "ChatGPT",
            "description": "OpenAI 开发的大型语言模型，提供自然语言对话和内容生成能力",
            "url": "https://chat.openai.com",
            "icon": "🤖",
            "category": ToolCategory.AI_CHAT
        },
        {
            "name": "Claude",
            "description": "Anthropic 开发的 AI 助手，擅长长文本处理和分析",
            "url": "https://claude.ai",
            "icon": "🧠",
            "category": ToolCategory.AI_CHAT
        },
        {
            "name": "Bard",
            "description": "Google 开发的 AI 对话助手，集成 Google 搜索能力",
            "url": "https://bard.google.com",
            "icon": "🎭",
            "category": ToolCategory.AI_CHAT
        },
        
        # 提示词工具类
        {
            "name": "PromptPerfect",
            "description": "AI提示词优化工具，帮助改进提示词效果",
            "url": "https://promptperfect.jina.ai",
            "icon": "✨",
            "category": ToolCategory.PROMPT
        },
        {
            "name": "MidJourney Prompt Helper",
            "description": "专门用于生成和优化 MidJourney 提示词的工具",
            "url": "https://midjourney-prompt-helper.netlify.app",
            "icon": "🎨",
            "category": ToolCategory.PROMPT
        },
        
        # 图像生成类
        {
            "name": "Midjourney",
            "description": "强大的 AI 图像生成工具，特别擅长艺术风格图像",
            "url": "https://www.midjourney.com",
            "icon": "🎨",
            "category": ToolCategory.IMAGE
        },
        {
            "name": "DALL·E",
            "description": "OpenAI 开发的 AI 图像生成工具，擅长创意和写实风格",
            "url": "https://labs.openai.com",
            "icon": "🖼️",
            "category": ToolCategory.IMAGE
        },
        {
            "name": "Stable Diffusion",
            "description": "开源的 AI 图像生成模型，支持本地部署",
            "url": "https://stability.ai",
            "icon": "🎯",
            "category": ToolCategory.IMAGE
        },
        
        # 视频生成类
        {
            "name": "Runway",
            "description": "AI 视频编辑和生成工具，支持多种创意效果",
            "url": "https://runway.ml",
            "icon": "🎥",
            "category": ToolCategory.VIDEO
        },
        {
            "name": "Synthesia",
            "description": "AI 数字人视频生成平台，用于创建教育和营销视频",
            "url": "https://www.synthesia.io",
            "icon": "🎬",
            "category": ToolCategory.VIDEO
        },
        
        # 音频处理类
        {
            "name": "Murf",
            "description": "AI 语音生成工具，支持多种语言和声音风格",
            "url": "https://murf.ai",
            "icon": "🎤",
            "category": ToolCategory.AUDIO
        },
        {
            "name": "Descript",
            "description": "AI 驱动的音频编辑工具，支持转录和声音克隆",
            "url": "https://www.descript.com",
            "icon": "🎧",
            "category": ToolCategory.AUDIO
        },
        
        # 代码开发类
        {
            "name": "GitHub Copilot",
            "description": "AI 代码助手，提供实时代码建议和自动完成",
            "url": "https://github.com/features/copilot",
            "icon": "👨‍💻",
            "category": ToolCategory.CODE
        },
        {
            "name": "Amazon CodeWhisperer",
            "description": "亚马逊开发的 AI 代码助手，支持多种编程语言",
            "url": "https://aws.amazon.com/codewhisperer",
            "icon": "💻",
            "category": ToolCategory.CODE
        },
        
        # 写作助手类
        {
            "name": "Grammarly",
            "description": "AI 写作助手，提供语法检查和写作建议",
            "url": "https://www.grammarly.com",
            "icon": "✍️",
            "category": ToolCategory.WRITING
        },
        {
            "name": "Jasper",
            "description": "AI 内容创作平台，用于营销文案和博客写作",
            "url": "https://www.jasper.ai",
            "icon": "📝",
            "category": ToolCategory.WRITING
        },
        
        # ... 继续添加更多工具 ...
    ]
    
    for tool_data in tools:
        db_tool = Tool(
            user_id=user_id,
            **tool_data
        )
        db.add(db_tool)
    
    db.commit() 