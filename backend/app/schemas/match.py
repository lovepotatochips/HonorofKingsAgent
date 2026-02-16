# 导入Pydantic的BaseModel类
# BaseModel是Pydantic的核心类，用于创建数据验证和序列化模型
from pydantic import BaseModel

# 导入类型提示
from typing import List, Optional, Dict, Any

# 导入datetime类，用于处理日期时间
from datetime import datetime


class MatchData(BaseModel):
    """
    对局数据模型
    
    用于接收和验证对局数据
    
    功能:
        - 验证对局数据的格式
        - 提供数据类型转换
        - 确保数据的完整性
    
    使用场景:
        - 用户上传对局数据
        - API端点的请求体验证
        - 对局数据录入
    
    字段说明:
        user_id: 用户ID（必填）
        hero_id: 英雄ID（可选）
        hero_name: 英雄名称（可选）
        position: 位置（可选）
        result: 对局结果（可选）
        duration: 对局时长（可选）
        kills: 击杀数（可选，默认0）
        deaths: 死亡数（可选，默认0）
        assists: 助攻数（可选，默认0）
        gold: 获得金币（可选，默认0）
        damage: 造成伤害（可选，默认0）
        damage_taken: 承受伤害（可选，默认0）
        healing: 治疗量（可选，默认0）
        participation_rate: 参团率（可选，默认0.0）
        kda: KDA比率（可选，默认0.0）
        equipment_list: 装备列表（可选）
        inscription: 铭文配置（可选）
        rank: 段位（可选）
        screenshot_url: 截图URL（可选）
    """
    
    # 用户ID
    # str: 字符串类型
    # 必填字段，没有默认值
    # 用途: 标识对局所属的用户
    user_id: str
    
    # 英雄ID
    # Optional[int]: 可选的整数类型，默认为None
    # 用途: 使用的英雄ID
    hero_id: Optional[int] = None
    
    # 英雄名称
    # Optional[str]: 可选的字符串类型，默认为None
    # 用途: 使用的英雄名称
    # 示例: "鲁班七号"
    hero_name: Optional[str] = None
    
    # 位置
    # Optional[str]: 可选的字符串类型，默认为None
    # 用途: 对局中的位置
    # 示例: "top"（上路）、"jungle"（打野）、"mid"（中路）、"archer"（发育路）、"support"（辅助）
    position: Optional[str] = None
    
    # 对局结果
    # Optional[str]: 可选的字符串类型，默认为None
    # 用途: 对局的胜负情况
    # 示例: "victory"（胜利）、"defeat"（失败）、"draw"（平局）
    result: Optional[str] = None
    
    # 对局时长
    # Optional[int]: 可选的整数类型，默认为None
    # 用途: 对局持续的时间（秒）
    # 示例: 1200 表示20分钟
    duration: Optional[int] = None
    
    # 击杀数
    # Optional[int]: 可选的整数类型，默认为0
    # 用途: 本局击杀的敌人数量
    kills: Optional[int] = 0
    
    # 死亡数
    # Optional[int]: 可选的整数类型，默认为0
    # 用途: 本局死亡次数
    deaths: Optional[int] = 0
    
    # 助攻数
    # Optional[int]: 可选的整数类型，默认为0
    # 用途: 本局助攻次数
    assists: Optional[int] = 0
    
    # 获得金币
    # Optional[int]: 可选的整数类型，默认为0
    # 用途: 本局获得的总金币
    gold: Optional[int] = 0
    
    # 造成伤害
    # Optional[int]: 可选的整数类型，默认为0
    # 用途: 对敌方英雄造成的总伤害
    damage: Optional[int] = 0
    
    # 承受伤害
    # Optional[int]: 可选的整数类型，默认为0
    # 用途: 本局承受的总伤害
    damage_taken: Optional[int] = 0
    
    # 治疗量
    # Optional[int]: 可选的整数类型，默认为0
    # 用途: 对队友的总治疗量
    healing: Optional[int] = 0
    
    # 参团率
    # Optional[float]: 可选的浮点数类型，默认为0.0
    # 用途: 参团率，计算公式：（击杀+助攻）/团队总击杀数
    # 示例: 0.7 表示70%的参团率
    participation_rate: Optional[float] = 0.0
    
    # KDA比率
    # Optional[float]: 可选的浮点数类型，默认为0.0
    # 用途: KDA比率，计算公式：（击杀+助攻）/最大（死亡，1）
    # 示例: 5.0 表示平均每次死亡造成5个击杀或助攻
    kda: Optional[float] = 0.0
    
    # 装备列表
    # Optional[List[Dict[str, Any]]]: 可选的字典列表，默认为None
    # 用途: 本局购买的装备
    # 示例: [
    #   {"id": 1, "name": "无尽战刃", "order": 1},
    #   {"id": 2, "name": "影刃", "order": 2}
    # ]
    equipment_list: Optional[List[Dict[str, Any]]] = None
    
    # 铭文配置
    # Optional[Dict[str, Any]]: 可选的字典，默认为None
    # 用途: 本局使用的铭文配置
    # 示例: {
    #   "red": [{"id": 1, "name": "无双", "count": 10}],
    #   "blue": [{"id": 2, "name": "鹰眼", "count": 10}],
    #   "green": [{"id": 3, "name": "夺萃", "count": 10}]
    # }
    inscription: Optional[Dict[str, Any]] = None
    
    # 段位
    # Optional[str]: 可选的字符串类型，默认为None
    # 用途: 对局时的段位
    # 示例: "钻石II"、"星耀III"
    rank: Optional[str] = None
    
    # 截图URL
    # Optional[str]: 可选的字符串类型，默认为None
    # 用途: 对局结束后的截图链接
    screenshot_url: Optional[str] = None


class MatchSummary(BaseModel):
    """
    对局摘要模型
    
    用于返回对局的摘要信息
    
    功能:
        - 序列化对局摘要数据
        - 提供轻量级的对局信息
        - 用于对局列表展示
    
    使用场景:
        - 对局历史列表
        - 对局统计
        - 数据分析
    
    字段说明:
        id: 对局ID
        hero_name: 英雄名称
        position: 位置
        result: 对局结果
        duration: 对局时长
        kda: KDA比率
        participation_rate: 参团率
        created_at: 创建时间
    """
    
    # 对局ID
    # str: 字符串类型
    # 必填字段，没有默认值
    # 用途: 对局的唯一标识符
    id: str
    
    # 英雄名称
    # str: 字符串类型
    # 必填字段，没有默认值
    # 用途: 本局使用的英雄名称
    hero_name: str
    
    # 位置
    # Optional[str]: 可选的字符串类型，可以为None
    # 用途: 本局的位置
    # 示例: "top"、"jungle"、"mid"、"archer"、"support"
    position: Optional[str]
    
    # 对局结果
    # Optional[str]: 可选的字符串类型，可以为None
    # 用途: 本局的胜负情况
    # 示例: "victory"、"defeat"、"draw"
    result: Optional[str]
    
    # 对局时长
    # Optional[int]: 可选的整数类型，可以为None
    # 用途: 本局的持续时间（秒）
    duration: Optional[int]
    
    # KDA比率
    # float: 浮点数类型
    # 必填字段，没有默认值
    # 用途: 本局的KDA数据
    kda: float
    
    # 参团率
    # float: 浮点数类型
    # 必填字段，没有默认值
    # 用途: 本局的参团率
    participation_rate: float
    
    # 创建时间
    # datetime: 日期时间类型
    # 必填字段，没有默认值
    # 用途: 对局记录的创建时间
    created_at: datetime
    
    class Config:
        """
        Pydantic配置类
        """
        # from_attributes: 允许从ORM对象创建Pydantic模型
        # True: 可以将SQLAlchemy模型转换为Pydantic模型
        from_attributes = True
