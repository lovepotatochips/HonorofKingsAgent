"""
业务逻辑层包初始化模块

这个模块是services包的初始化文件，用于将services目录标记为Python包。

功能:
    - 将services目录标记为Python包
    - 导出所有业务逻辑服务类
    - 供API端点调用

包含的服务:
    - chat_service: 聊天服务，处理AI对话逻辑
    - ai_service: AI服务，调用GLM-4模型
    - hero_service: 英雄服务，处理英雄相关业务
    - intent_service: 意图识别服务
    - match_service: 对局服务
    - analysis_service: 分析服务
    - user_service: 用户服务

设计模式:
    - 服务层模式（Service Layer）
    - 将业务逻辑与数据访问分离

使用示例:
    from app.services import ChatService, HeroService, UserService
"""
