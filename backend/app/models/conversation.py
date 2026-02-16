# 导入SQLAlchemy的Column类，用于定义表的列
# Column是ORM中定义字段的基本单位
from sqlalchemy import Column, String, DateTime, Text, JSON, Integer, ForeignKey

# 导入relationship函数，用于定义表之间的关系
# relationship用于建立ORM对象之间的关系（一对多、多对多等）
from sqlalchemy.orm import relationship

# 导入datetime类，用于处理日期时间
from datetime import datetime

# 导入Base基类，所有ORM模型都继承自Base
from app.core.database import Base


class Conversation(Base):
    """
    对话模型
    
    表示用户与AI的对话记录
    
    数据库表名: conversations
    
    主要功能:
        - 存储用户与AI的对话历史
        - 记录用户的意图和上下文
        - 关联用户、英雄、对局等实体
    
    字段说明:
        id: 对话记录唯一标识符
        user_id: 关联的用户ID
        user_message: 用户发送的消息
        ai_response: AI的回复
        intent: 对话意图类型
        context: 对话上下文
        hero_id: 关联的英雄ID（如对话涉及特定英雄）
        match_id: 关联的对局ID（如对话涉及特定对局）
        created_at: 对话创建时间
    
    关系:
        user: 对话与用户的多对一关系
    """
    
    # ==================== 表定义 ====================
    
    # 指定数据库表名
    # SQL: CREATE TABLE conversations (...)
    __tablename__ = "conversations"
    
    # ==================== 主键字段 ====================
    
    # 对话记录ID，主键
    # primary_key=True: 该字段是表的主键，唯一标识一条记录
    # index=True: 为该字段创建索引，加快查询速度
    # Integer: 整数类型，自增主键
    id = Column(Integer, primary_key=True, index=True)
    
    # ==================== 关联字段 ====================
    
    # 用户ID，外键关联到users表
    # String(50): 字符串类型，最大长度50
    # ForeignKey("users.id"): 外键，关联到users表的id字段
    # nullable=False: 不能为空，必须指定用户
    # index=True: 创建索引，加快按用户查询对话的速度
    user_id = Column(String(50), ForeignKey("users.id"), nullable=False, index=True)
    
    # ==================== 对话内容字段 ====================
    
    # 用户发送的消息内容
    # Text: 文本类型，可以存储大量文本
    # nullable=False: 不能为空，必须有消息内容
    # 用途: 存储用户的原始问题或输入
    user_message = Column(Text, nullable=False)
    
    # AI的回复内容
    # Text: 文本类型，可以存储大量文本
    # nullable=True (默认): 可以为空（如AI回复失败时）
    # 用途: 存储AI生成的回复内容
    ai_response = Column(Text)
    
    # ==================== 智能分析字段 ====================
    
    # 对话意图类型
    # String(50): 字符串类型，最大长度50
    # 用途: 记录用户问题的意图，便于后续分析和优化
    # 示例: "hero_query"（英雄查询）、"equipment_query"（装备查询）、"strategy_query"（策略查询）
    intent = Column(String(50))
    
    # 对话上下文
    # JSON: JSON类型，可以存储复杂的数据结构
    # 用途: 存储对话的上下文信息，支持多轮对话
    # 示例: {
    #   "previous_messages": [
    #     {"role": "user", "content": "上一条消息"},
    #     {"role": "assistant", "content": "上一条回复"}
    #   ],
    #   "entities": {
    #     "hero": "鲁班七号",
    #     "position": "archer"
    #   }
    # }
    context = Column(JSON)
    
    # ==================== 关联实体字段 ====================
    
    # 关联的英雄ID
    # Integer: 整数类型
    # ForeignKey("heroes.id"): 外键，关联到heroes表的id字段
    # nullable=True (默认): 可以为空，不是所有对话都涉及特定英雄
    # 用途: 当对话涉及特定英雄时，记录英雄ID，便于后续分析
    hero_id = Column(Integer, ForeignKey("heroes.id"))
    
    # 关联的对局ID
    # String(50): 字符串类型，最大长度50
    # nullable=True (默认): 可以为空，不是所有对话都涉及特定对局
    # 用途: 当对话涉及特定对局时，记录对局ID，便于后续分析
    match_id = Column(String(50))
    
    # ==================== 时间戳字段 ====================
    
    # 对话创建时间
    # DateTime: 日期时间类型
    # default=datetime.utcnow: 默认值为当前UTC时间
    # index=True: 创建索引，加快按时间查询对话的速度
    # 用途: 记录对话发生的时间，用于排序和历史查询
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # ==================== 关系定义 ====================
    
    # 对话与用户的多对一关系
    # 多条对话记录属于一个用户
    # relationship: 定义ORM关系
    # "User": 关联的模型类名
    # back_populates="conversations": 指向User模型中名为"conversations"的反向关系
    user = relationship("User", back_populates="conversations")
