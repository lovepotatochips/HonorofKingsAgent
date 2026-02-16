# 导入SQLAlchemy的Column类，用于定义表的列
# Column是ORM中定义字段的基本单位
from sqlalchemy import Column, String, DateTime, JSON, Integer

# 导入relationship函数，用于定义表之间的关系
# relationship用于建立ORM对象之间的关系（一对多、多对多等）
from sqlalchemy.orm import relationship

# 导入datetime类，用于处理日期时间
from datetime import datetime

# 导入Base基类，所有ORM模型都继承自Base
from app.core.database import Base


class User(Base):
    """
    用户模型
    
    表示应用中的用户实体，存储用户的基本信息和游戏数据
    
    数据库表名: users
    
    主要功能:
        - 存储用户基本信息（昵称、头像、段位等）
        - 管理用户与对话、对局的关系
        - 存储用户偏好设置
    
    字段说明:
        id: 用户唯一标识符
        nickname: 用户昵称
        avatar: 用户头像URL
        rank: 游戏段位
        stars: 段位星数
        favorite_heroes: 常用英雄列表
        preferences: 用户偏好设置
        created_at: 账户创建时间
        updated_at: 最后更新时间
    
    关系:
        conversations: 用户与对话的一对多关系
        matches: 用户与对局的一对多关系
    """
    
    # ==================== 表定义 ====================
    
    # 指定数据库表名
    # SQL: CREATE TABLE users (...)
    __tablename__ = "users"
    
    # ==================== 主键字段 ====================
    
    # 用户ID，主键
    # primary_key=True: 该字段是表的主键，唯一标识一条记录
    # index=True: 为该字段创建索引，加快查询速度
    # String(50): 字符串类型，最大长度50
    id = Column(String(50), primary_key=True, index=True)
    
    # ==================== 基本信息字段 ====================
    
    # 用户昵称
    # String(50): 字符串类型，最大长度50
    # nullable=True (默认): 可以为空
    nickname = Column(String(50))
    
    # 用户头像URL
    # String(200): 字符串类型，最大长度200（存储图片URL）
    avatar = Column(String(200))
    
    # ==================== 游戏数据字段 ====================
    
    # 游戏段位
    # String(50): 字符串类型，存储如"钻石"、"星耀"等
    rank = Column(String(50))
    
    # 段位星数
    # Integer: 整数类型，默认值为0
    # default=0: 如果不指定，默认为0
    stars = Column(Integer, default=0)
    
    # ==================== 数据字段 ====================
    
    # 常用英雄列表
    # JSON: JSON类型，可以存储复杂的数据结构
    # 用途: 存储用户最常使用的英雄ID列表
    # 示例: [1, 2, 3, 4, 5]
    favorite_heroes = Column(JSON)
    
    # 用户偏好设置
    # JSON: JSON类型，存储键值对
    # 用途: 存储用户的个性化设置
    # 示例: {"theme": "dark", "notifications": true}
    preferences = Column(JSON)
    
    # ==================== 时间戳字段 ====================
    
    # 账户创建时间
    # DateTime: 日期时间类型
    # default=datetime.utcnow: 默认值为当前UTC时间
    # 用途: 记录用户注册时间，用于数据分析
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 最后更新时间
    # DateTime: 日期时间类型
    # default=datetime.utcnow: 默认值为当前UTC时间
    # onupdate=datetime.utcnow: 每次更新记录时自动设置为当前时间
    # 用途: 记录用户信息的最后修改时间
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # ==================== 关系定义 ====================
    
    # 用户与对话的一对多关系
    # 一个用户可以有多条对话记录
    # relationship: 定义ORM关系
    # "Conversation": 关联的模型类名
    # back_populates="user": 指向Conversation模型中名为"user"的反向关系
    # cascade="all, delete-orphan": 级联操作
    #   - all: 所有操作（增删改）都会级联
    #   - delete-orphan: 当用户被删除时，自动删除关联的对话
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    
    # 用户与对局的一对多关系
    # 一个用户可以有多场对局记录
    # relationship: 定义ORM关系
    # "Match": 关联的模型类名
    # back_populates="user": 指向Match模型中名为"user"的反向关系
    # cascade="all, delete-orphan": 级联操作
    #   - all: 所有操作都会级联
    #   - delete-orphan: 当用户被删除时，自动删除关联的对局
    matches = relationship("Match", back_populates="user", cascade="all, delete-orphan")
