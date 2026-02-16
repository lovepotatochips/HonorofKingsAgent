# 导入类型提示
# List: 列表类型
# Optional: 可选类型（可以为None）
# Dict: 字典类型
# Any: 任意类型
from typing import List, Optional, Dict, Any

# 导入Session类
# Session: SQLAlchemy的数据库会话，用于与数据库交互
from sqlalchemy.orm import Session

# 导入聊天相关的Schema
# ChatRequest: 聊天请求模型
# ChatResponse: 聊天响应模型
# MessageHistory: 消息历史模型
from app.schemas.chat import ChatRequest, ChatResponse, MessageHistory

# 导入对话模型
# Conversation: 数据库中的对话记录表映射类
from app.models.conversation import Conversation

# 导入AI服务
# AIService: AI对话服务，负责生成AI回复
from app.services.ai_service import AIService

# 导入意图识别服务
# IntentService: 意图识别服务，负责识别用户问题类型
from app.services.intent_service import IntentService


class ChatService:
    """
    聊天服务类
    
    负责处理用户与AI的对话
    
    主要功能:
        - 处理用户发送的消息
        - 识别用户意图
        - 生成AI回复
        - 保存对话历史
        - 提供对话建议
    
    设计模式:
        - 服务层模式（Service Layer）
        - 协调AI服务和意图识别服务
        - 管理对话上下文
    
    使用场景:
        - 用户与AI对话
        - 对话历史查询
        - 对话历史清理
    """
    
    def __init__(self):
        """
        初始化聊天服务
        
        功能:
            - 创建AI服务实例
            - 创建意图识别服务实例
        
        设计模式:
            - 依赖注入（Dependency Injection）
            - 将依赖的服务在构造函数中初始化
        """
        # 创建AI服务实例
        # 负责生成AI回复
        self.ai_service = AIService()
        
        # 创建意图识别服务实例
        # 负责识别用户问题的意图
        self.intent_service = IntentService()
    
    async def process_message(
        self,
        request: ChatRequest,
        db: Session
    ) -> ChatResponse:
        """
        处理用户消息
        
        参数:
            request: 聊天请求，包含用户消息、上下文等信息
            db: 数据库会话对象
        
        返回:
            ChatResponse: 聊天响应，包含AI回复、意图识别结果等
        
        功能:
            - 识别用户消息的意图
            - 根据意图生成AI回复
            - 保存对话记录到数据库
            - 生成相关建议
            - 提取相关英雄
        
        业务逻辑:
            1. 识别用户消息的意图
            2. 限制上下文长度为最近5轮
            3. 调用AI服务生成回复
            4. 保存对话记录到数据库
            5. 生成相关建议
            6. 提取相关英雄
            7. 返回响应
        
        异步处理:
            - async: 异步方法，不阻塞主线程
            - await: 等待AI服务的异步响应
        """
        # 识别用户消息的意图
        # 调用意图识别服务，返回意图识别结果
        intent_result = self.intent_service.recognize(request.message)
        
        # 限制对话上下文长度
        # 只保留最近5轮对话，避免上下文过长
        # 如果上下文超过5轮，截取最后5轮
        # 如果上下文不超过5轮，使用全部上下文
        context = request.context[-5:] if len(request.context) > 5 else request.context
        
        # 调用AI服务生成回复
        # await: 等待异步操作完成
        # 传入用户消息、意图、上下文和英雄ID
        ai_response = await self.ai_service.generate_response(
            message=request.message,
            intent=intent_result.intent,
            context=context,
            hero_id=request.hero_id
        )
        
        # 创建对话记录对象
        conversation = Conversation(
            # 用户ID
            user_id=request.user_id,
            # 用户消息
            user_message=request.message,
            # AI回复
            ai_response=ai_response,
            # 识别的意图
            intent=intent_result.intent,
            # 对话上下文
            context=context,
            # 关联的英雄ID（可选）
            hero_id=request.hero_id,
            # 关联的对局ID（可选）
            match_id=request.match_id
        )
        
        # 将对话记录添加到数据库会话
        db.add(conversation)
        # 提交事务，保存对话记录
        db.commit()
        
        # 生成相关建议
        # 根据识别的意图生成后续建议
        suggestions = self._generate_suggestions(intent_result.intent)
        
        # 提取相关英雄
        # 从AI回复中提取相关英雄ID
        related_heroes = self._extract_related_heroes(ai_response)
        
        # 返回聊天响应对象
        return ChatResponse(
            # AI回复内容
            response=ai_response,
            # 识别的意图
            intent=intent_result.intent,
            # 意图识别的置信度
            confidence=intent_result.confidence,
            # 相关建议列表
            suggestions=suggestions,
            # 相关英雄ID列表
            related_heroes=related_heroes
        )
    
    async def get_history(
        self,
        user_id: str,
        limit: int,
        db: Session
    ) -> List[MessageHistory]:
        """
        获取用户的对话历史
        
        参数:
            user_id: 用户ID
            limit: 返回的记录数量限制
            db: 数据库会话对象
        
        返回:
            List[MessageHistory]: 对话历史列表
        
        功能:
            - 查询用户的对话记录
            - 按时间倒序排列
            - 限制返回的记录数量
        
        业务逻辑:
            1. 根据用户ID查询对话记录
            2. 按创建时间倒序排列（最新的在前）
            3. 限制返回的记录数量
            4. 转换为消息历史对象列表
        
        异步处理:
            - async: 异步方法，不阻塞主线程
        """
        # 从数据库查询对话记录
        # filter: 添加查询条件（用户ID等于指定值）
        # order_by: 按创建时间倒序排列（desc()表示降序）
        # limit(): 限制返回的记录数量
        # all(): 获取所有匹配的记录
        conversations = db.query(Conversation).filter(
            Conversation.user_id == user_id
        ).order_by(Conversation.created_at.desc()).limit(limit).all()
        
        # 将数据库记录转换为消息历史对象列表
        # 使用列表推导式，简洁高效
        return [
            MessageHistory(
                id=conv.id,
                user_message=conv.user_message,
                # 如果AI回复为空，使用空字符串
                ai_response=conv.ai_response or "",
                intent=conv.intent,
                created_at=conv.created_at
            )
            for conv in conversations
        ]
    
    async def clear_history(self, user_id: str, db: Session):
        """
        清除用户的对话历史
        
        参数:
            user_id: 用户ID
            db: 数据库会话对象
        
        返回:
            None
        
        功能:
            - 删除用户的所有对话记录
            - 用于用户清理对话历史
        
        业务逻辑:
            1. 根据用户ID删除所有对话记录
            2. 提交事务
        
        注意:
            - 此操作不可逆，请谨慎使用
            - 删除后无法恢复
        
        异步处理:
            - async: 异步方法，不阻塞主线程
        """
        # 删除用户的所有对话记录
        # filter: 添加查询条件（用户ID等于指定值）
        # delete(): 删除所有匹配的记录
        db.query(Conversation).filter(
            Conversation.user_id == user_id
        ).delete()
        
        # 提交事务，保存删除操作
        db.commit()
    
    def _generate_suggestions(self, intent: str) -> List[str]:
        """
        生成相关建议
        
        参数:
            intent: 识别的意图类型
        
        返回:
            List[str]: 建议列表
        
        功能:
            - 根据识别的意图生成后续建议
            - 帮助用户进行后续提问
        
        业务逻辑:
            1. 根据意图类型查找对应的建议
            2. 如果没有找到，返回默认建议
        
        私有方法:
            - 以下划线开头，表示内部方法
            - 只在类内部使用，不对外暴露
        """
        # 定义意图与建议的映射关系
        # key: 意图类型
        # value: 建议列表
        suggestions_map = {
            # 装备相关的建议
            "equipment": ["查看铭文搭配", "查看对位英雄", "查看出装思路"],
            
            # 铭文相关的建议
            "inscription": ["查看出装推荐", "查看技能连招", "查看对位英雄"],
            
            # BP建议相关的建议
            "bp_suggestion": ["查看当前阵容短板", "查看禁选建议", "查看counter位推荐"],
            
            # 对局分析相关的建议
            "match_analysis": ["查看详细数据", "查看改进建议", "分享对局"],
            
            # 野怪计时相关的建议
            "monster_timer": ["开启野怪计时", "查看技能冷却", "查看开团时机"],
            
            # 娱乐互动相关的建议
            "entertainment": ["英雄语音对话", "趣味问答", "战绩卡片"]
        }
        
        # 根据意图获取对应的建议
        # 如果意图不在映射中，返回默认建议
        return suggestions_map.get(intent, ["换个问题试试", "查看英雄资料", "查看出装推荐"])
    
    def _extract_related_heroes(self, response: str) -> Optional[List[int]]:
        """
        提取相关英雄
        
        参数:
            response: AI回复内容
        
        返回:
            Optional[List[int]]: 相关英雄ID列表，如果没有则返回None
        
        功能:
            - 从AI回复中提取相关英雄ID
            - 用于后续的英雄推荐
        
        业务逻辑:
            - 当前实现返回None
            - 可以通过正则表达式或NLP技术提取英雄名称
        
        私有方法:
            - 以下划线开头，表示内部方法
            - 只在类内部使用，不对外暴露
        
        扩展方向:
            - 可以实现实体识别
            - 可以使用NLP技术提取英雄名称
            - 可以建立英雄名称与ID的映射表
        """
        # 当前实现返回None
        # 未来可以扩展为实际的英雄提取逻辑
        return None
