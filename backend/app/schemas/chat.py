# 导入Pydantic的BaseModel和Field类
# BaseModel: 创建数据验证和序列化模型
# Field: 为字段提供额外的验证和元数据
from pydantic import BaseModel, Field

# 导入类型提示
from typing import List, Optional, Dict, Any

# 导入datetime类，用于处理日期时间
from datetime import datetime


class ChatRequest(BaseModel):
    """
    聊天请求模型
    
    用于接收用户发送的聊天消息
    
    功能:
        - 验证用户发送的聊天请求
        - 提供字段验证
        - 确保必填字段存在
    
    使用场景:
        - 用户发送消息给AI
        - API端点的请求体验证
    
    字段说明:
        user_id: 用户ID（必填）
        message: 用户消息内容（必填）
        context: 对话上下文（可选，默认为空列表）
        hero_id: 关联的英雄ID（可选）
        match_id: 关联的对局ID（可选）
    """
    
    # 用户ID
    # str: 字符串类型
    # 必填字段，没有默认值
    # 用途: 标识发送消息的用户
    user_id: str
    
    # 用户消息内容
    # str: 字符串类型
    # 必填字段，没有默认值
    # 用途: 用户想要询问或表达的内容
    message: str
    
    # 对话上下文
    # Optional[List[Dict[str, Any]]]: 可选的字典列表类型，默认为空列表
    # 用途: 保存之前的对话历史，支持多轮对话
    # 示例: [
    #   {"role": "user", "content": "你好"},
    #   {"role": "assistant", "content": "你好，有什么可以帮你的？"}
    # ]
    context: Optional[List[Dict[str, Any]]] = []
    
    # 关联的英雄ID
    # Optional[int]: 可选的整数类型，默认为None
    # 用途: 如果对话涉及特定英雄，记录英雄ID
    # 示例: 1（鲁班七号的ID）
    hero_id: Optional[int] = None
    
    # 关联的对局ID
    # Optional[str]: 可选的字符串类型，默认为None
    # 用途: 如果对话涉及特定对局，记录对局ID
    # 示例: "match_12345"
    match_id: Optional[str] = None


class ChatResponse(BaseModel):
    """
    聊天响应模型
    
    用于返回AI的回复内容
    
    功能:
        - 定义AI回复的数据结构
        - 包含意图识别结果
        - 提供相关建议
    
    使用场景:
        - 返回AI的回复给前端
        - API端点的响应体
    
    字段说明:
        response: AI回复内容
        intent: 识别的意图类型
        confidence: 意图识别的置信度
        suggestions: 相关建议列表
        related_heroes: 相关英雄ID列表
    """
    
    # AI回复内容
    # str: 字符串类型
    # 必填字段，没有默认值
    # 用途: AI生成的回复内容
    # 示例: "鲁班七号是一个远程物理输出英雄，主要走发育路..."
    response: str
    
    # 识别的意图类型
    # str: 字符串类型
    # 必填字段，没有默认值
    # 用途: 识别用户问题的类型
    # 示例: "hero_query"（英雄查询）、"equipment_query"（装备查询）、"strategy_query"（策略查询）
    intent: str
    
    # 意图识别的置信度
    # float: 浮点数类型
    # 必填字段，没有默认值
    # 用途: 表示意图识别的可信程度，范围0-1
    # 示例: 0.95 表示95%的置信度
    confidence: float
    
    # 相关建议列表
    # Optional[List[str]]: 可选的字符串列表类型，默认为空列表
    # 用途: 提供相关的后续建议
    # 示例: ["鲁班七号怎么出装？", "鲁班七号适合什么铭文？"]
    suggestions: Optional[List[str]] = []
    
    # 相关英雄ID列表
    # Optional[List[int]]: 可选的整数列表类型，默认为空列表
    # 用途: 提供相关的英雄推荐
    # 示例: [1, 2, 3]
    related_heroes: Optional[List[int]] = []


class MessageHistory(BaseModel):
    """
    消息历史模型
    
    用于表示对话历史记录
    
    功能:
        - 序列化对话历史数据
        - 将数据库记录转换为API响应格式
    
    使用场景:
        - 返回用户的对话历史
        - 显示聊天记录
    
    字段说明:
        id: 消息记录ID
        user_message: 用户发送的消息
        ai_response: AI的回复
        intent: 对话意图
        created_at: 创建时间
    """
    
    # 消息记录ID
    # int: 整数类型
    # 必填字段，没有默认值
    # 用途: 对话记录的唯一标识符
    id: int
    
    # 用户发送的消息
    # str: 字符串类型
    # 必填字段，没有默认值
    # 用途: 用户的原始消息内容
    user_message: str
    
    # AI的回复
    # str: 字符串类型
    # 必填字段，没有默认值
    # 用途: AI生成的回复内容
    ai_response: str
    
    # 对话意图
    # Optional[str]: 可选的字符串类型，可以为None
    # 用途: 记录对话的意图类型
    intent: Optional[str]
    
    # 创建时间
    # datetime: 日期时间类型
    # 必填字段，没有默认值
    # 用途: 记录对话发生的时间
    created_at: datetime
    
    class Config:
        """
        Pydantic配置类
        """
        # from_attributes: 允许从ORM对象创建Pydantic模型
        # True: 可以将SQLAlchemy模型转换为Pydantic模型
        from_attributes = True


class IntentResult(BaseModel):
    """
    意图识别结果模型
    
    用于表示意图识别的结果
    
    功能:
        - 存储意图识别的结果
        - 包含实体提取信息
        - 提供置信度评分
    
    使用场景:
        - 意图识别服务的返回结果
        - 上下文管理
    
    字段说明:
        intent: 识别的意图类型
        confidence: 识别的置信度
        entities: 提取的实体信息
    """
    
    # 识别的意图类型
    # str: 字符串类型
    # 必填字段，没有默认值
    # 用途: 用户问题的意图分类
    # 示例: "hero_query"（英雄查询）、"equipment_query"（装备查询）、"match_analysis"（对局分析）
    intent: str
    
    # 识别的置信度
    # float: 浮点数类型
    # 必填字段，没有默认值
    # 用途: 表示意图识别的可信程度，范围0-1
    # 示例: 0.9 表示90%的置信度
    confidence: float
    
    # 提取的实体信息
    # Dict[str, Any]: 字典类型，键为字符串，值为任意类型
    # 必填字段，没有默认值
    # 用途: 从用户问题中提取的关键实体
    # 示例: {
    #   "hero": "鲁班七号",
    #   "position": "archer",
    #   "skill": "大招"
    # }
    entities: Dict[str, Any]
