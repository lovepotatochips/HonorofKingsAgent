# 导入FastAPI相关模块
# APIRouter: 用于创建API路由
# Depends: 用于依赖注入
# HTTPException: 用于处理HTTP异常
from fastapi import APIRouter, Depends, HTTPException

# 导入Session类
# Session: SQLAlchemy的数据库会话，用于与数据库交互
from sqlalchemy.orm import Session

# 导入类型提示
# List: 列表类型
from typing import List

# 导入数据库依赖
# get_db: 获取数据库会话的依赖函数
from app.core.database import get_db

# 导入聊天服务
# ChatService: 聊天服务，负责处理聊天逻辑
from app.services.chat_service import ChatService

# 导入聊天相关的Schema
# ChatRequest: 聊天请求模型
# ChatResponse: 聊天响应模型
# MessageHistory: 消息历史模型
from app.schemas.chat import ChatRequest, ChatResponse, MessageHistory

# 创建API路由器
router = APIRouter()

# 创建聊天服务实例
chat_service = ChatService()


@router.post("/send", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    发送聊天消息
    
    参数:
        request: 聊天请求，包含用户消息、上下文等信息
        db: 数据库会话对象（通过依赖注入自动获取）
    
    返回:
        ChatResponse: 聊天响应，包含AI回复、意图识别结果等
    
    功能:
        - 接收用户发送的消息
        - 识别用户意图
        - 生成AI回复
        - 保存对话记录
        - 返回聊天响应
    
    业务逻辑:
        1. 调用聊天服务处理消息
        2. 返回聊天响应
        3. 如果发生异常，返回500错误
    
    HTTP方法:
        - POST: 用于发送数据
    
    路径:
        - /api/v1/chat/send
    """
    try:
        # 调用聊天服务处理消息
        # await: 等待异步操作完成
        response = await chat_service.process_message(request, db)
        return response
    except Exception as e:
        # 如果发生异常，返回500错误
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{user_id}", response_model=List[MessageHistory])
async def get_chat_history(
    user_id: str,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    获取聊天历史
    
    参数:
        user_id: 用户ID（路径参数）
        limit: 返回的记录数量限制（查询参数，默认20）
        db: 数据库会话对象（通过依赖注入自动获取）
    
    返回:
        List[MessageHistory]: 聊天历史列表
    
    功能:
        - 查询用户的对话历史
        - 按时间倒序排列
        - 限制返回的记录数量
    
    业务逻辑:
        1. 调用聊天服务获取历史记录
        2. 返回聊天历史列表
        3. 如果发生异常，返回500错误
    
    HTTP方法:
        - GET: 用于获取数据
    
    路径:
        - /api/v1/chat/history/{user_id}
    """
    try:
        # 调用聊天服务获取历史记录
        history = await chat_service.get_history(user_id, limit, db)
        return history
    except Exception as e:
        # 如果发生异常，返回500错误
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/history/{user_id}")
async def clear_chat_history(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    清除聊天历史
    
    参数:
        user_id: 用户ID（路径参数）
        db: 数据库会话对象（通过依赖注入自动获取）
    
    返回:
        dict: 操作结果消息
    
    功能:
        - 删除用户的所有对话记录
        - 用于用户清理对话历史
    
    业务逻辑:
        1. 调用聊天服务清除历史记录
        2. 返回成功消息
        3. 如果发生异常，返回500错误
    
    HTTP方法:
        - DELETE: 用于删除数据
    
    路径:
        - /api/v1/chat/history/{user_id}
    
    注意:
        - 此操作不可逆，请谨慎使用
    """
    try:
        # 调用聊天服务清除历史记录
        await chat_service.clear_history(user_id, db)
        # 返回成功消息
        return {"message": "对话历史已清除"}
    except Exception as e:
        # 如果发生异常，返回500错误
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/intents")
async def get_intents():
    """
    获取意图列表
    
    返回:
        dict: 意图列表和快捷命令
    
    功能:
        - 返回支持的意图类型
        - 返回快捷命令列表
        - 用于前端展示意图选择和快捷操作
    
    意图类型:
        - equipment: 出装推荐
        - inscription: 铭文搭配
        - bp_suggestion: BP建议
        - match_analysis: 复盘分析
        - monster_timer: 野怪计时
        - entertainment: 娱乐问答
    
    快捷命令:
        - 我的常用英雄出装
        - 当前版本强势英雄
        - BP阵容建议
        - 对局复盘
    
    HTTP方法:
        - GET: 用于获取数据
    
    路径:
        - /api/v1/chat/intents
    """
    # 返回意图列表和快捷命令
    return {
        # 意图列表
        "intents": [
            {"id": "equipment", "name": "出装推荐", "description": "查询英雄出装推荐"},
            {"id": "inscription", "name": "铭文搭配", "description": "查询英雄铭文搭配"},
            {"id": "bp_suggestion", "name": "BP建议", "description": "获取阵容BP建议"},
            {"id": "match_analysis", "name": "复盘分析", "description": "对局复盘分析"},
            {"id": "monster_timer", "name": "野怪计时", "description": "野怪计时提醒"},
            {"id": "entertainment", "name": "娱乐问答", "description": "趣味问答"}
        ],
        # 快捷命令列表
        "quick_commands": [
            {"command": "我的常用英雄出装", "description": "查询常用英雄出装"},
            {"command": "当前版本强势英雄", "description": "查询版本强势英雄"},
            {"command": "BP阵容建议", "description": "获取BP建议"},
            {"command": "对局复盘", "description": "开始复盘分析"}
        ]
    }
