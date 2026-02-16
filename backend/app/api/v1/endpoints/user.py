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

# 导入用户相关的Schema
# UserProfile: 用户资料模型
# UserPreferences: 用户偏好设置模型
from app.schemas.user import UserProfile, UserPreferences

# 创建API路由器
router = APIRouter()


@router.get("/profile/{user_id}", response_model=UserProfile)
async def get_user_profile(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    获取用户资料
    
    参数:
        user_id: 用户ID（路径参数）
        db: 数据库会话对象（通过依赖注入自动获取）
    
    返回:
        UserProfile: 用户资料对象
    
    功能:
        - 查询用户的资料信息
        - 返回用户的基本信息
    
    业务逻辑:
        1. 调用用户服务获取用户资料
        2. 如果用户不存在，返回404错误
        3. 如果用户存在，返回用户资料
        4. 如果发生异常，返回500错误
    
    HTTP方法:
        - GET: 用于获取数据
    
    路径:
        - /api/v1/user/profile/{user_id}
    """
    try:
        # 导入用户服务
        # 在方法内部导入，避免循环导入
        from app.services.user_service import UserService
        
        # 创建用户服务实例
        user_service = UserService()
        
        # 调用用户服务获取用户资料
        profile = user_service.get_profile(user_id, db)
        
        # 如果用户不存在，返回404错误
        if not profile:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        return profile
    except HTTPException:
        # 如果是HTTP异常，直接抛出
        raise
    except Exception as e:
        # 如果发生其他异常，返回500错误
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/profile/{user_id}", response_model=UserProfile)
async def update_user_profile(
    user_id: str,
    profile: UserProfile,
    db: Session = Depends(get_db)
):
    """
    更新用户资料
    
    参数:
        user_id: 用户ID（路径参数）
        profile: 用户资料数据（请求体）
        db: 数据库会话对象（通过依赖注入自动获取）
    
    返回:
        UserProfile: 更新后的用户资料对象
    
    功能:
        - 更新用户的资料信息
        - 如果用户不存在则自动创建
    
    业务逻辑:
        1. 调用用户服务更新用户资料
        2. 返回更新后的用户资料
        3. 如果发生异常，返回500错误
    
    HTTP方法:
        - PUT: 用于更新数据
    
    路径:
        - /api/v1/user/profile/{user_id}
    """
    try:
        # 导入用户服务
        # 在方法内部导入，避免循环导入
        from app.services.user_service import UserService
        
        # 创建用户服务实例
        user_service = UserService()
        
        # 调用用户服务更新用户资料
        updated_profile = user_service.update_profile(user_id, profile, db)
        return updated_profile
    except Exception as e:
        # 如果发生异常，返回500错误
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/preferences/{user_id}", response_model=UserPreferences)
async def get_user_preferences(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    获取用户偏好设置
    
    参数:
        user_id: 用户ID（路径参数）
        db: 数据库会话对象（通过依赖注入自动获取）
    
    返回:
        UserPreferences: 用户偏好设置对象
    
    功能:
        - 查询用户的偏好设置
        - 如果用户不存在，返回默认设置
    
    业务逻辑:
        1. 调用用户服务获取用户偏好设置
        2. 返回用户偏好设置
        3. 如果发生异常，返回500错误
    
    HTTP方法:
        - GET: 用于获取数据
    
    路径:
        - /api/v1/user/preferences/{user_id}
    """
    try:
        # 导入用户服务
        # 在方法内部导入，避免循环导入
        from app.services.user_service import UserService
        
        # 创建用户服务实例
        user_service = UserService()
        
        # 调用用户服务获取用户偏好设置
        preferences = user_service.get_preferences(user_id, db)
        return preferences
    except Exception as e:
        # 如果发生异常，返回500错误
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/preferences/{user_id}", response_model=UserPreferences)
async def update_user_preferences(
    user_id: str,
    preferences: UserPreferences,
    db: Session = Depends(get_db)
):
    """
    更新用户偏好设置
    
    参数:
        user_id: 用户ID（路径参数）
        preferences: 用户偏好设置数据（请求体）
        db: 数据库会话对象（通过依赖注入自动获取）
    
    返回:
        UserPreferences: 更新后的用户偏好设置对象
    
    功能:
        - 更新用户的偏好设置
        - 如果用户不存在则自动创建
    
    业务逻辑:
        1. 调用用户服务更新用户偏好设置
        2. 返回更新后的用户偏好设置
        3. 如果发生异常，返回500错误
    
    HTTP方法:
        - PUT: 用于更新数据
    
    路径:
        - /api/v1/user/preferences/{user_id}
    """
    try:
        # 导入用户服务
        # 在方法内部导入，避免循环导入
        from app.services.user_service import UserService
        
        # 创建用户服务实例
        user_service = UserService()
        
        # 调用用户服务更新用户偏好设置
        updated = user_service.update_preferences(user_id, preferences, db)
        return updated
    except Exception as e:
        # 如果发生异常，返回500错误
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/data/{user_id}")
async def clear_user_data(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    清除用户数据
    
    参数:
        user_id: 用户ID（路径参数）
        db: 数据库会话对象（通过依赖注入自动获取）
    
    返回:
        dict: 操作结果消息
    
    功能:
        - 删除用户的所有数据
        - 包括对话记录、对局记录和用户账户
        - 用于用户注销或数据清理
    
    业务逻辑:
        1. 调用用户服务清除用户数据
        2. 返回成功消息
        3. 如果发生异常，返回500错误
    
    HTTP方法:
        - DELETE: 用于删除数据
    
    路径:
        - /api/v1/user/data/{user_id}
    
    注意:
        - 此操作不可逆，请谨慎使用
    """
    try:
        # 导入用户服务
        # 在方法内部导入，避免循环导入
        from app.services.user_service import UserService
        
        # 创建用户服务实例
        user_service = UserService()
        
        # 调用用户服务清除用户数据
        user_service.clear_all_data(user_id, db)
        
        # 返回成功消息
        return {"message": "用户数据已清除"}
    except Exception as e:
        # 如果发生异常，返回500错误
        raise HTTPException(status_code=500, detail=str(e))
