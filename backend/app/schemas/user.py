# 导入Pydantic的BaseModel类
# BaseModel是Pydantic的核心类，用于创建数据验证和序列化模型
# Pydantic是一个数据验证库，可以自动验证和转换数据
from pydantic import BaseModel

# 导入类型提示
# List: 列表类型
# Optional: 可选类型（可以为None）
# Dict: 字典类型
# Any: 任意类型
from typing import List, Optional, Dict, Any


class UserProfile(BaseModel):
    """
    用户资料模型
    
    用于API请求和响应中的用户数据验证和序列化
    
    功能:
        - 验证用户数据是否符合要求
        - 将数据库模型转换为API响应格式
        - 自动进行数据类型转换
    
    使用场景:
        - 返回用户信息给前端
        - 接收和验证用户数据
    
    字段说明:
        id: 用户ID（必填）
        nickname: 用户昵称（可选）
        avatar: 用户头像URL（可选）
        rank: 游戏段位（可选）
        stars: 段位星数（必填，默认0）
        favorite_heroes: 常用英雄列表（可选）
    """
    
    # 用户ID
    # str: 字符串类型
    # 必填字段，没有默认值
    # 用途: 用户的唯一标识符
    id: str
    
    # 用户昵称
    # Optional[str]: 可选的字符串类型，可以为None
    # 用途: 用户在应用中显示的昵称
    nickname: Optional[str]
    
    # 用户头像URL
    # Optional[str]: 可选的字符串类型，可以为None
    # 用途: 用户头像图片的链接地址
    avatar: Optional[str]
    
    # 游戏段位
    # Optional[str]: 可选的字符串类型，可以为None
    # 用途: 用户在王者荣耀游戏中的段位
    # 示例: "钻石II"、"星耀III"
    rank: Optional[str]
    
    # 段位星数
    # int: 整数类型
    # 必填字段，数据库默认值为0
    # 用途: 当前段位的星数
    # 示例: 0-5星
    stars: int
    
    # 常用英雄列表
    # Optional[List[int]]: 可选的整数列表类型，可以为None
    # 用途: 用户最常使用的英雄ID列表
    # 示例: [1, 2, 3, 4, 5]
    favorite_heroes: Optional[List[int]]
    
    class Config:
        """
        Pydantic配置类
        
        功能:
            - 配置模型的行为
            - 定义如何处理属性
        """
        # from_attributes: 允许从ORM对象创建Pydantic模型
        # True: 可以将SQLAlchemy模型转换为Pydantic模型
        # 用途: 在返回API响应时，自动将数据库模型转换为字典
        from_attributes = True


class UserPreferences(BaseModel):
    """
    用户偏好设置模型
    
    用于存储和验证用户的个人偏好设置
    
    功能:
        - 验证用户偏好设置数据
        - 提供默认值
        - 确保设置的有效性
    
    使用场景:
        - 更新用户偏好设置
        - 读取用户偏好设置
        - 前端配置界面的数据验证
    
    字段说明:
        voice_enabled: 是否启用语音功能
        voice_wake_word: 语音唤醒词
        float_window_enabled: 是否启用悬浮窗
        dark_mode: 是否启用深色模式
        sound_enabled: 是否启用声音
        vibration_enabled: 是否启用震动
        auto_clear_context: 是否自动清除对话上下文
        context_rounds: 保留的对话上下文轮数
    """
    
    # 是否启用语音功能
    # bool: 布尔类型，默认值为True
    # 用途: 控制AI对话是否支持语音输入
    voice_enabled: bool = True
    
    # 语音唤醒词
    # str: 字符串类型，默认值为"王者助手"
    # 用途: 用户说出这个词可以唤醒AI助手
    voice_wake_word: str = "王者助手"
    
    # 是否启用悬浮窗
    # bool: 布尔类型，默认值为True
    # 用途: 控制是否显示AI助手的悬浮窗
    float_window_enabled: bool = True
    
    # 是否启用深色模式
    # bool: 布尔类型，默认值为False
    # 用途: 控制应用是否使用深色主题
    dark_mode: bool = False
    
    # 是否启用声音
    # bool: 布尔类型，默认值为True
    # 用途: 控制应用是否播放提示音
    sound_enabled: bool = True
    
    # 是否启用震动
    # bool: 布尔类型，默认值为True
    # 用途: 控制应用是否震动提示
    vibration_enabled: bool = True
    
    # 是否自动清除对话上下文
    # bool: 布尔类型，默认值为False
    # 用途: 控制是否在对话结束后自动清除历史记录
    auto_clear_context: bool = False
    
    # 保留的对话上下文轮数
    # int: 整数类型，默认值为5
    # 用途: AI助手记住前几轮对话的内容
    # 示例: 5表示记住最近5轮对话
    context_rounds: int = 5


class UserCreate(BaseModel):
    """
    用户创建模型
    
    用于创建新用户时的数据验证
    
    功能:
        - 验证创建用户时的输入数据
        - 提供必需字段的验证
        - 允许可选字段
    
    使用场景:
        - 用户注册
        - 创建新用户账户
    
    字段说明:
        id: 用户ID（必填）
        nickname: 用户昵称（可选）
        avatar: 用户头像URL（可选）
    
    注意:
        - id是必填字段，用于唯一标识用户
        - nickname和avatar是可选字段，可以在创建后补充
    """
    
    # 用户ID
    # str: 字符串类型
    # 必填字段，没有默认值
    # 用途: 用户的唯一标识符
    id: str
    
    # 用户昵称
    # Optional[str]: 可选的字符串类型，默认值为None
    # 用途: 用户在应用中显示的昵称
    # 如果不提供，可以后续更新
    nickname: Optional[str] = None
    
    # 用户头像URL
    # Optional[str]: 可选的字符串类型，默认值为None
    # 用途: 用户头像图片的链接地址
    # 如果不提供，可以使用默认头像
    avatar: Optional[str] = None
