"""
数据验证模型包初始化模块

这个模块是schemas包的初始化文件，用于将schemas目录标记为Python包。

功能:
    - 将schemas目录标记为Python包
    - 导出所有数据验证模型类
    - 供API端点使用

包含的模型:
    - chat: 聊天相关的数据验证模型
    - hero: 英雄相关的数据验证模型
    - match: 对局相关的数据验证模型
    - analysis: 分析相关的数据验证模型
    - user: 用户相关的数据验证模型

技术栈:
    - Pydantic: 数据验证和序列化库

使用示例:
    from app.schemas import ChatRequest, HeroResponse, UserProfile
"""
