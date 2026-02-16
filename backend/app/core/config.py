# 导入Pydantic的BaseSettings类，用于创建配置类
# Pydantic是一个数据验证库，BaseSettings可以方便地从环境变量或配置文件中读取配置
from pydantic_settings import BaseSettings

# 导入字段验证器，用于对配置字段进行自定义验证
from pydantic import field_validator

# 导入类型提示，用于类型注解
from typing import List, Union

# 导入操作系统模块，用于读取环境变量
import os

# 导入LRU缓存装饰器，用于缓存配置对象
# LRU（Least Recently Used）是一种缓存策略，最近最少使用的项会被淘汰
from functools import lru_cache


class Settings(BaseSettings):
    """
    应用配置类
    
    继承自BaseSettings，可以从环境变量或.env文件中自动读取配置
    
    功能:
        - 集中管理所有配置项
        - 自动从环境变量读取配置
        - 提供配置验证
        - 支持类型转换
    """
    
    # ==================== 基础配置 ====================
    
    # 项目名称
    PROJECT_NAME: str = "王者荣耀智能助手"
    
    # 项目版本号
    VERSION: str = "1.0.0"
    
    # API版本前缀
    # 所有API路径都会加上这个前缀，如 /api/v1/heroes
    API_V1_STR: str = "/api/v1"
    
    # 调试模式标志
    # True: 开发模式，显示详细错误信息
    # False: 生产模式，隐藏详细错误信息
    DEBUG: bool = True
    
    # ==================== 数据库配置 ====================
    
    # 数据库连接URL
    # 格式: sqlite:///文件路径  或  mysql+pymysql://用户:密码@主机:端口/数据库
    DATABASE_URL: str
    
    # Redis连接URL（可选）
    # 用于缓存、会话存储等
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # ==================== AI服务配置 ====================
    
    # 智谱AI的API密钥
    # 需要从智谱AI官网申请
    ZHIPUAI_API_KEY: str
    
    # ==================== 安全配置 ====================
    
    # 密钥，用于JWT令牌签名
    # 在生产环境应该使用强随机字符串
    SECRET_KEY: str
    
    # 加密算法
    # HS256: HMAC SHA-256，一种对称加密算法
    ALGORITHM: str = "HS256"
    
    # 访问令牌过期时间（分钟）
    # 30分钟后令牌失效，需要重新登录
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # ==================== 环境配置 ====================
    
    # 运行环境
    # development: 开发环境
    # production: 生产环境
    ENVIRONMENT: str = "development"
    
    # 日志级别
    # DEBUG: 最详细的信息，用于调试
    # INFO: 一般信息
    # WARNING: 警告信息
    # ERROR: 错误信息
    LOG_LEVEL: str = "INFO"
    
    # ==================== CORS配置 ====================
    
    # 允许的跨域源列表
    # 允许哪些前端域名访问后端API
    # 列表中的每个元素都是一个允许的域名
    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:5173",      # 开发服务器
        "http://localhost:8080",      # 备用端口
        "http://127.0.0.1:5173"    # 本地回环地址
    ]
    
    # ==================== AI参数配置 ====================
    
    # AI最大token数
    # 限制AI回复的最大长度，控制成本
    AI_MAX_TOKENS: int = 2000
    
    # AI温度参数
    # 控制AI回复的随机性
    # 0.0: 最保守，回复最确定
    # 1.0: 最随机，回复最有创造性
    # 0.7: 平衡值，既有创造性又有确定性
    AI_TEMPERATURE: float = 0.7
    
    # AI Top-P参数
    # 核采样参数，控制从概率最高的前P%的词中选择
    # 0.9: 从概率最高的90%的词中选择
    AI_TOP_P: float = 0.9
    
    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """
        解析CORS配置字段
        
        参数:
            v: 配置值，可以是字符串或列表
        
        功能:
            - 支持从环境变量读取逗号分隔的字符串
            - 将字符串转换为列表
            - 保留列表格式不变
        
        示例:
            输入: "http://localhost:5173,http://localhost:8080"
            输出: ["http://localhost:5173", "http://localhost:8080"]
        """
        # 如果是字符串，按逗号分割并去除空格
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        # 如果是列表，直接返回
        return v
    
    class Config:
        """
        Pydantic配置内部类
        
        功能:
            - 指定环境变量文件
            - 设置大小写敏感性
        """
        # 环境变量文件名
        # Pydantic会从这个文件读取配置
        env_file = ".env"
        # 区分大小写
        # True: 环境变量名称区分大小写
        # False: 自动转换为小写
        case_sensitive = True


# 使用LRU缓存装饰器缓存配置对象
# 这确保配置只被加载一次，提高性能
@lru_cache()
def get_settings() -> Settings:
    """
    获取配置对象（单例模式）
    
    返回:
        Settings: 配置对象实例
    
    功能:
        - 使用LRU缓存，避免重复读取配置
        - 确保配置只被加载一次
        - 提高应用启动性能
    
    使用:
        from app.core.config import settings
        settings.DATABASE_URL
    """
    return Settings()


# 创建全局配置对象
# 其他模块通过导入这个对象来访问配置
settings = get_settings()
