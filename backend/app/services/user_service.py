# 导入类型提示
# Optional: 可选类型（可以为None）
from typing import Optional

# 导入Session类
# Session: SQLAlchemy的数据库会话，用于与数据库交互
from sqlalchemy.orm import Session

# 导入用户模型
# User: 数据库中的用户表映射类
from app.models.user import User

# 导入用户相关的Schema
# UserProfile: 用户资料模型
# UserPreferences: 用户偏好设置模型
# UserCreate: 用户创建模型
from app.schemas.user import UserProfile, UserPreferences, UserCreate

# 导入datetime类，用于处理日期时间
from datetime import datetime


class UserService:
    """
    用户服务类
    
    负责处理用户相关的业务逻辑
    
    主要功能:
        - 用户创建和管理
        - 用户资料的查询和更新
        - 用户偏好设置的读取和修改
        - 用户数据的清理
    
    设计模式:
        - 服务层模式（Service Layer）
        - 将业务逻辑与数据访问分离
        - 提供清晰的API供控制器调用
    
    使用场景:
        - 用户注册
        - 用户信息管理
        - 用户设置管理
        - 用户数据清理
    """
    
    def create_user(self, user_data: UserCreate, db: Session) -> UserProfile:
        """
        创建新用户
        
        参数:
            user_data: 用户创建数据，包含用户ID、昵称、头像等
            db: 数据库会话对象
        
        返回:
            UserProfile: 创建的用户资料对象
        
        功能:
            - 根据输入数据创建新用户
            - 设置默认的用户偏好设置
            - 将用户数据保存到数据库
            - 返回用户资料信息
        
        业务逻辑:
            1. 创建User模型实例
            2. 设置用户基本信息（ID、昵称、头像）
            3. 设置默认的偏好设置
            4. 保存到数据库
            5. 返回用户资料对象
        """
        # 创建用户模型实例
        # 使用传入的用户数据初始化用户对象
        user = User(
            # 设置用户ID
            id=user_data.id,
            # 设置用户昵称
            nickname=user_data.nickname,
            # 设置用户头像
            avatar=user_data.avatar,
            # 设置默认的用户偏好设置
            # 使用JSON格式存储偏好设置
            preferences={
                # 是否启用语音功能
                "voice_enabled": True,
                # 语音唤醒词
                "voice_wake_word": "王者助手",
                # 是否启用悬浮窗
                "float_window_enabled": True,
                # 是否启用深色模式
                "dark_mode": False,
                # 是否启用声音
                "sound_enabled": True,
                # 是否启用震动
                "vibration_enabled": True,
                # 是否自动清除对话上下文
                "auto_clear_context": False,
                # 保留的对话上下文轮数
                "context_rounds": 5
            }
        )
        
        # 将用户添加到数据库会话
        db.add(user)
        # 提交事务，将数据保存到数据库
        db.commit()
        # 刷新用户对象，获取数据库生成的ID等信息
        db.refresh(user)
        
        # 返回用户资料对象
        # 将数据库模型转换为Schema对象
        return UserProfile(
            id=user.id,
            nickname=user.nickname,
            avatar=user.avatar,
            rank=user.rank,
            stars=user.stars,
            favorite_heroes=user.favorite_heroes
        )
    
    def get_profile(self, user_id: str, db: Session) -> Optional[UserProfile]:
        """
        获取用户资料
        
        参数:
            user_id: 用户ID
            db: 数据库会话对象
        
        返回:
            UserProfile: 用户资料对象，如果用户不存在则返回None
        
        功能:
            - 根据用户ID查询用户资料
            - 返回用户的基本信息
        
        业务逻辑:
            1. 根据user_id查询数据库
            2. 如果用户不存在，返回None
            3. 如果用户存在，返回用户资料对象
        """
        # 从数据库查询用户
        # filter: 添加查询条件（用户ID等于指定值）
        # first(): 获取第一条记录，如果没有则返回None
        user = db.query(User).filter(User.id == user_id).first()
        
        # 如果用户不存在，返回None
        if not user:
            return None
        
        # 用户存在，返回用户资料对象
        return UserProfile(
            id=user.id,
            nickname=user.nickname,
            avatar=user.avatar,
            rank=user.rank,
            stars=user.stars,
            favorite_heroes=user.favorite_heroes
        )
    
    def update_profile(self, user_id: str, profile: UserProfile, db: Session) -> UserProfile:
        """
        更新用户资料
        
        参数:
            user_id: 用户ID
            profile: 用户资料数据
            db: 数据库会话对象
        
        返回:
            UserProfile: 更新后的用户资料对象
        
        功能:
            - 更新用户的基本信息
            - 如果用户不存在则自动创建
            - 保存更新后的数据
        
        业务逻辑:
            1. 查询用户是否存在
            2. 如果不存在，创建新用户
            3. 更新用户资料信息
            4. 更新修改时间
            5. 保存到数据库
            6. 返回更新后的资料
        """
        # 从数据库查询用户
        user = db.query(User).filter(User.id == user_id).first()
        
        # 如果用户不存在，创建新用户
        if not user:
            user = User(id=user_id)
            # 将新用户添加到数据库会话
            db.add(user)
        
        # 更新用户资料信息
        user.nickname = profile.nickname
        user.avatar = profile.avatar
        user.rank = profile.rank
        user.stars = profile.stars
        user.favorite_heroes = profile.favorite_heroes
        # 更新修改时间为当前时间
        user.updated_at = datetime.utcnow()
        
        # 提交事务，保存更改
        db.commit()
        # 刷新用户对象
        db.refresh(user)
        
        # 返回更新后的用户资料对象
        return UserProfile(
            id=user.id,
            nickname=user.nickname,
            avatar=user.avatar,
            rank=user.rank,
            stars=user.stars,
            favorite_heroes=user.favorite_heroes
        )
    
    def get_preferences(self, user_id: str, db: Session) -> UserPreferences:
        """
        获取用户偏好设置
        
        参数:
            user_id: 用户ID
            db: 数据库会话对象
        
        返回:
            UserPreferences: 用户偏好设置对象
        
        功能:
            - 查询用户的偏好设置
            - 如果用户不存在，返回默认设置
            - 如果用户存在但没有偏好设置，使用默认值
        
        业务逻辑:
            1. 查询用户是否存在
            2. 如果不存在，返回默认偏好设置
            3. 如果存在，读取用户偏好设置
            4. 使用默认值填充缺失的设置
        """
        # 从数据库查询用户
        user = db.query(User).filter(User.id == user_id).first()
        
        # 如果用户不存在，返回默认偏好设置
        if not user:
            return UserPreferences()
        
        # 获取用户的偏好设置，如果为空则使用空字典
        prefs = user.preferences or {}
        
        # 返回用户偏好设置对象
        # 使用get方法，如果key不存在则使用默认值
        return UserPreferences(
            voice_enabled=prefs.get("voice_enabled", True),
            voice_wake_word=prefs.get("voice_wake_word", "王者助手"),
            float_window_enabled=prefs.get("float_window_enabled", True),
            dark_mode=prefs.get("dark_mode", False),
            sound_enabled=prefs.get("sound_enabled", True),
            vibration_enabled=prefs.get("vibration_enabled", True),
            auto_clear_context=prefs.get("auto_clear_context", False),
            context_rounds=prefs.get("context_rounds", 5)
        )
    
    def update_preferences(self, user_id: str, preferences: UserPreferences, db: Session) -> UserPreferences:
        """
        更新用户偏好设置
        
        参数:
            user_id: 用户ID
            preferences: 用户偏好设置数据
            db: 数据库会话对象
        
        返回:
            UserPreferences: 更新后的用户偏好设置对象
        
        功能:
            - 更新用户的偏好设置
            - 如果用户不存在则自动创建
            - 保存更新后的设置
        
        业务逻辑:
            1. 查询用户是否存在
            2. 如果不存在，创建新用户
            3. 将偏好设置转换为字典
            4. 更新用户的偏好设置
            5. 更新修改时间
            6. 保存到数据库
            7. 返回更新后的设置
        """
        # 从数据库查询用户
        user = db.query(User).filter(User.id == user_id).first()
        
        # 如果用户不存在，创建新用户
        if not user:
            user = User(id=user_id)
            # 将新用户添加到数据库会话
            db.add(user)
        
        # 将偏好设置转换为字典格式
        user.preferences = {
            "voice_enabled": preferences.voice_enabled,
            "voice_wake_word": preferences.voice_wake_word,
            "float_window_enabled": preferences.float_window_enabled,
            "dark_mode": preferences.dark_mode,
            "sound_enabled": preferences.sound_enabled,
            "vibration_enabled": preferences.vibration_enabled,
            "auto_clear_context": preferences.auto_clear_context,
            "context_rounds": preferences.context_rounds
        }
        # 更新修改时间为当前时间
        user.updated_at = datetime.utcnow()
        
        # 提交事务，保存更改
        db.commit()
        
        # 返回更新后的偏好设置对象
        return preferences
    
    def clear_all_data(self, user_id: str, db: Session):
        """
        清除用户的所有数据
        
        参数:
            user_id: 用户ID
            db: 数据库会话对象
        
        返回:
            None
        
        功能:
            - 删除用户的所有对话记录
            - 删除用户的所有对局记录
            - 删除用户账户
            - 用于用户注销或数据清理
        
        业务逻辑:
            1. 删除用户的所有对话记录
            2. 删除用户的所有对局记录
            3. 删除用户账户
            4. 提交事务
        
        注意:
            - 此操作不可逆，请谨慎使用
            - 删除顺序很重要（先删除子记录，再删除父记录）
        """
        # 导入相关的模型
        # 在方法内部导入，避免循环导入
        from app.models.conversation import Conversation
        from app.models.match import Match
        
        # 删除用户的所有对话记录
        # filter: 添加查询条件（用户ID等于指定值）
        # delete(): 删除所有匹配的记录
        db.query(Conversation).filter(Conversation.user_id == user_id).delete()
        
        # 删除用户的所有对局记录
        db.query(Match).filter(Match.user_id == user_id).delete()
        
        # 删除用户账户
        db.query(User).filter(User.id == user_id).delete()
        
        # 提交事务，保存所有删除操作
        db.commit()
