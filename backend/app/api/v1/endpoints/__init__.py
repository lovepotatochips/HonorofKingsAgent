"""
API端点包初始化模块

这个模块是endpoints包的初始化文件，用于将endpoints目录标记为Python包。

功能:
    - 将endpoints目录标记为Python包
    - 导出所有API端点路由器
    - 供api/v1/__init__.py注册使用

包含的端点:
    - chat: 聊天API端点
    - hero: 英雄API端点
    - user: 用户API端点
    - match: 对局API端点
    - analysis: 分析API端点

使用示例:
    from app.api.v1.endpoints import chat, hero, user, match, analysis
"""
