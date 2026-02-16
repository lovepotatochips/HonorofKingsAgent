"""
核心配置包初始化模块

这个模块是core包的初始化文件，用于将core目录标记为Python包。

功能:
    - 将core目录标记为Python包
    - 导出核心配置和数据库相关功能
    - 供其他模块使用

包含的模块:
    - config: 应用配置，包含API密钥、数据库连接等配置
    - database: 数据库配置，包含数据库引擎和会话管理

使用示例:
    from app.core import settings, get_db
    from app.core.database import init_db
"""
