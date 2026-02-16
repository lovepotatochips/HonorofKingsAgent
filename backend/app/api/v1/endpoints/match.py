# 导入FastAPI相关模块
# APIRouter: 用于创建API路由
# Depends: 用于依赖注入
# HTTPException: 用于处理HTTP异常
from fastapi import APIRouter, Depends, HTTPException

# 导入Session类
# Session: SQLAlchemy的数据库会话，用于与数据库交互
from sqlalchemy.orm import Session

# 导入数据库依赖
# get_db: 获取数据库会话的依赖函数
from app.core.database import get_db

# 导入对局相关的Schema
# MatchData: 对局数据模型
# MatchSummary: 对局摘要模型
from app.schemas.match import MatchData, MatchSummary

# 创建API路由器
router = APIRouter()


@router.post("/import")
async def import_match_data(
    match_data: MatchData,
    db: Session = Depends(get_db)
):
    """
    导入对局数据
    
    参数:
        match_data: 对局数据（请求体）
        db: 数据库会话对象（通过依赖注入自动获取）
    
    返回:
        dict: 导入结果，包含对局ID和消息
    
    功能:
        - 导入对局数据到数据库
        - 生成对局ID
        - 保存对局信息
    
    业务逻辑:
        1. 调用对局服务导入对局数据
        2. 返回导入结果
        3. 如果发生异常，返回500错误
    
    HTTP方法:
        - POST: 用于发送数据
    
    路径:
        - /api/v1/match/import
    
    异步处理:
        - async: 异步方法，不阻塞主线程
    """
    try:
        # 导入对局服务
        # 在方法内部导入，避免循环导入
        from app.services.match_service import MatchService
        
        # 创建对局服务实例
        match_service = MatchService()
        
        # 调用对局服务导入对局数据
        # await: 等待异步操作完成
        result = await match_service.import_match(match_data, db)
        return result
    except Exception as e:
        # 如果发生异常，返回500错误
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{user_id}")
async def get_match_history(
    user_id: str,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    获取对局历史
    
    参数:
        user_id: 用户ID（路径参数）
        limit: 返回的记录数量限制（查询参数，默认10）
        db: 数据库会话对象（通过依赖注入自动获取）
    
    返回:
        List[MatchSummary]: 对局历史列表
    
    功能:
        - 查询用户的对局历史
        - 按时间倒序排列
        - 限制返回的记录数量
    
    业务逻辑:
        1. 调用对局服务获取对局历史
        2. 返回对局历史列表
        3. 如果发生异常，返回500错误
    
    HTTP方法:
        - GET: 用于获取数据
    
    路径:
        - /api/v1/match/history/{user_id}
    """
    try:
        # 导入对局服务
        # 在方法内部导入，避免循环导入
        from app.services.match_service import MatchService
        
        # 创建对局服务实例
        match_service = MatchService()
        
        # 调用对局服务获取对局历史
        history = match_service.get_history(user_id, limit, db)
        return history
    except Exception as e:
        # 如果发生异常，返回500错误
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summary/{match_id}", response_model=MatchSummary)
async def get_match_summary(
    match_id: str,
    db: Session = Depends(get_db)
):
    """
    获取对局摘要
    
    参数:
        match_id: 对局ID（路径参数）
        db: 数据库会话对象（通过依赖注入自动获取）
    
    返回:
        MatchSummary: 对局摘要对象
    
    功能:
        - 查询对局的摘要信息
        - 返回对局的基本数据
    
    业务逻辑:
        1. 调用对局服务获取对局摘要
        2. 如果对局不存在，返回404错误
        3. 如果对局存在，返回对局摘要
        4. 如果发生异常，返回500错误
    
    HTTP方法:
        - GET: 用于获取数据
    
    路径:
        - /api/v1/match/summary/{match_id}
    """
    try:
        # 导入对局服务
        # 在方法内部导入，避免循环导入
        from app.services.match_service import MatchService
        
        # 创建对局服务实例
        match_service = MatchService()
        
        # 调用对局服务获取对局摘要
        summary = match_service.get_summary(match_id, db)
        
        # 如果对局不存在，返回404错误
        if not summary:
            raise HTTPException(status_code=404, detail="对局记录不存在")
        
        return summary
    except HTTPException:
        # 如果是HTTP异常，直接抛出
        raise
    except Exception as e:
        # 如果发生其他异常，返回500错误
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{match_id}")
async def delete_match(
    match_id: str,
    db: Session = Depends(get_db)
):
    """
    删除对局记录
    
    参数:
        match_id: 对局ID（路径参数）
        db: 数据库会话对象（通过依赖注入自动获取）
    
    返回:
        dict: 操作结果消息
    
    功能:
        - 删除指定的对局记录
        - 用于用户清理对局历史
    
    业务逻辑:
        1. 调用对局服务删除对局记录
        2. 返回成功消息
        3. 如果发生异常，返回500错误
    
    HTTP方法:
        - DELETE: 用于删除数据
    
    路径:
        - /api/v1/match/{match_id}
    
    注意:
        - 此操作不可逆，请谨慎使用
    """
    try:
        # 导入对局服务
        # 在方法内部导入，避免循环导入
        from app.services.match_service import MatchService
        
        # 创建对局服务实例
        match_service = MatchService()
        
        # 调用对局服务删除对局记录
        match_service.delete_match(match_id, db)
        
        # 返回成功消息
        return {"message": "对局记录已删除"}
    except Exception as e:
        # 如果发生异常，返回500错误
        raise HTTPException(status_code=500, detail=str(e))
