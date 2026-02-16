# 导入Pydantic的BaseModel和Field类
# BaseModel: 创建数据验证和序列化模型
# Field: 为字段提供额外的验证和元数据
from pydantic import BaseModel, Field

# 导入类型提示
from typing import List, Optional, Dict, Any

# 导入datetime类，用于处理日期时间
from datetime import datetime


class Skill(BaseModel):
    """
    技能模型
    
    用于表示英雄的技能信息
    
    功能:
        - 存储技能的基本信息
        - 验证技能数据
        - 用于API请求和响应
    
    使用场景:
        - 英雄详情展示
        - 技能查询
        - 技能推荐
    
    字段说明:
        name: 技能名称
        description: 技能描述
        cooldown: 冷却时间（可选）
        cost: 消耗（可选）
        type: 技能类型（可选）
    """
    
    # 技能名称
    # str: 字符串类型
    # 必填字段，没有默认值
    # 用途: 技能的名称
    # 示例: "秘术·影"、"影刃"、"暗袭"
    name: str
    
    # 技能描述
    # str: 字符串类型
    # 必填字段，没有默认值
    # 用途: 技能的效果说明
    # 示例: "兰陵王向指定方向位移，并在进入隐身状态..."
    description: str
    
    # 冷却时间
    # Optional[str]: 可选的字符串类型，默认为None
    # 用途: 技能的冷却时间
    # 示例: "8" 表示8秒
    cooldown: Optional[str] = None
    
    # 消耗
    # Optional[str]: 可选的字符串类型，默认为None
    # 用途: 使用技能所需的消耗（如法力值）
    # 示例: "50" 表示50点法力值
    cost: Optional[str] = None
    
    # 技能类型
    # Optional[str]: 可选的字符串类型，默认为None
    # 用途: 技能的类型分类
    # 示例: "主动"、"被动"
    type: Optional[str] = None


class HeroResponse(BaseModel):
    """
    英雄响应模型（简版）
    
    用于返回英雄的基本信息
    
    功能:
        - 序列化英雄数据
        - 提供轻量级的英雄信息
        - 用于英雄列表展示
    
    使用场景:
        - 英雄列表页
        - 英雄搜索
        - 英雄推荐
    
    字段说明:
        id: 英雄ID
        name: 英雄名称
        title: 英雄称号
        position: 英雄定位
        difficulty: 难度等级
        image_url: 英雄图片URL
        win_rate: 胜率
        pick_rate: 选用率
        ban_rate: 禁用率
    """
    
    # 英雄ID
    # int: 整数类型
    # 必填字段，没有默认值
    # 用途: 英雄的唯一标识符
    id: int
    
    # 英雄名称
    # str: 字符串类型
    # 必填字段，没有默认值
    # 用途: 英雄的名称
    name: str
    
    # 英雄称号
    # Optional[str]: 可选的字符串类型，可以为None
    # 用途: 英雄的官方称号
    # 示例: "无敌剑圣"、"暗影刺客"
    title: Optional[str]
    
    # 英雄定位
    # Optional[str]: 可选的字符串类型，可以为None
    # 用途: 英雄在游戏中的主要定位
    # 示例: "tank"（坦克）、"warrior"（战士）、"mage"（法师）、"archer"（射手）、"support"（辅助）
    position: Optional[str]
    
    # 难度等级
    # Optional[str]: 可选的字符串类型，可以为None
    # 用途: 英雄的操作难度等级
    # 示例: "简单"、"普通"、"困难"、"超难"
    difficulty: Optional[str]
    
    # 英雄图片URL
    # Optional[str]: 可选的字符串类型，可以为None
    # 用途: 英雄的头像、立绘等图片链接
    image_url: Optional[str]
    
    # 胜率
    # float: 浮点数类型
    # 必填字段，没有默认值
    # 用途: 英雄的对局胜率，单位为百分比
    # 示例: 0.52 表示52%的胜率
    win_rate: float
    
    # 选用率
    # float: 浮点数类型
    # 必填字段，没有默认值
    # 用途: 英雄在BP阶段的选用率，单位为百分比
    # 示例: 0.35 表示35%的选用率
    pick_rate: float
    
    # 禁用率
    # float: 浮点数类型
    # 必填字段，没有默认值
    # 用途: 英雄在BP阶段的禁用率，单位为百分比
    # 示例: 0.15 表示15%的禁用率
    ban_rate: float
    
    class Config:
        """
        Pydantic配置类
        """
        # from_attributes: 允许从ORM对象创建Pydantic模型
        from_attributes = True


class HeroDetailResponse(BaseModel):
    """
    英雄详情响应模型（完整版）
    
    用于返回英雄的完整信息
    
    功能:
        - 序列化英雄的完整数据
        - 包含技能、克制关系等详细信息
        - 用于英雄详情页
    
    使用场景:
        - 英雄详情页
        - 英雄对比
        - 英雄教学
    
    字段说明:
        id: 英雄ID
        name: 英雄名称
        title: 英雄称号
        position: 英雄定位
        difficulty: 难度等级
        description: 英雄描述
        image_url: 英雄图片URL
        skills: 主动技能列表
        passive_skill: 被动技能
        win_rate: 胜率
        pick_rate: 选用率
        ban_rate: 禁用率
        counter_heroes: 克制的英雄列表
        countered_by_heroes: 被克制的英雄列表
    """
    
    # 英雄ID
    id: int
    
    # 英雄名称
    name: str
    
    # 英雄称号
    title: Optional[str]
    
    # 英雄定位
    position: Optional[str]
    
    # 难度等级
    difficulty: Optional[str]
    
    # 英雄描述
    # Optional[str]: 可选的字符串类型，可以为None
    # 用途: 英雄的背景故事、玩法介绍等
    description: Optional[str]
    
    # 英雄图片URL
    image_url: Optional[str]
    
    # 主动技能列表
    # List[Skill]: 技能对象列表
    # 必填字段，没有默认值
    # 用途: 英雄的所有主动技能
    # 示例: [Skill对象1, Skill对象2, Skill对象3]
    skills: List[Skill]
    
    # 被动技能
    # Optional[Skill]: 可选的技能对象，可以为None
    # 用途: 英雄的被动技能
    passive_skill: Optional[Skill]
    
    # 胜率
    win_rate: float
    
    # 选用率
    pick_rate: float
    
    # 禁用率
    ban_rate: float
    
    # 克制的英雄列表
    # Optional[List[str]]: 可选的字符串列表，可以为None
    # 用途: 该英雄克制的其他英雄名称列表
    # 示例: ["鲁班七号", "后羿", "妲己"]
    counter_heroes: Optional[List[str]]
    
    # 被克制的英雄列表
    # Optional[List[str]]: 可选的字符串列表，可以为None
    # 用途: 克制该英雄的其他英雄名称列表
    # 示例: ["张良", "东皇太一", "妲己"]
    countered_by_heroes: Optional[List[str]]
    
    class Config:
        """
        Pydantic配置类
        """
        from_attributes = True


class EquipmentResponse(BaseModel):
    """
    装备推荐响应模型
    
    用于返回英雄的装备推荐方案
    
    功能:
        - 序列化装备推荐数据
        - 提供装备方案和统计数据
        - 用于装备推荐展示
    
    使用场景:
        - 英雄详情页的装备推荐
        - 装备查询
        - 装备搭配建议
    
    字段说明:
        id: 推荐方案ID
        rank: 适用段位
        position: 适用位置
        equipment_list: 装备列表
        win_rate: 胜率
        pick_rate: 选用率
    """
    
    # 推荐方案ID
    # int: 整数类型
    # 必填字段，没有默认值
    # 用途: 装备推荐方案的唯一标识符
    id: int
    
    # 适用段位
    # str: 字符串类型
    # 必填字段，没有默认值
    # 用途: 该装备方案适用的段位
    # 示例: "青铜"、"黄金"、"钻石"、"星耀"、"王者"
    rank: str
    
    # 适用位置
    # Optional[str]: 可选的字符串类型，可以为None
    # 用途: 该装备方案适用的位置
    # 示例: "top"（上路）、"jungle"（打野）、"mid"（中路）、"archer"（发育路）、"support"（辅助）
    position: Optional[str]
    
    # 装备列表
    # List[Dict[str, Any]]: 字典列表
    # 必填字段，没有默认值
    # 用途: 装备推荐的详细信息
    # 示例: [
    #   {"id": 1, "name": "暗影战斧", "order": 1},
    #   {"id": 2, "name": "抵抗之靴", "order": 2}
    # ]
    equipment_list: List[Dict[str, Any]]
    
    # 胜率
    # float: 浮点数类型
    # 必填字段，没有默认值
    # 用途: 使用该装备方案的胜率
    win_rate: float
    
    # 选用率
    # float: 浮点数类型
    # 必填字段，没有默认值
    # 用途: 该装备方案的使用频率
    pick_rate: float
    
    class Config:
        """
        Pydantic配置类
        """
        from_attributes = True


class InscriptionResponse(BaseModel):
    """
    铭文推荐响应模型
    
    用于返回英雄的铭文推荐方案
    
    功能:
        - 序列化铭文推荐数据
        - 提供铭文配置和说明
        - 用于铭文推荐展示
    
    使用场景:
        - 英雄详情页的铭文推荐
        - 铭文查询
        - 铭文搭配建议
    
    字段说明:
        id: 推荐方案ID
        rank: 适用段位
        inscription_name: 铭文页名称
        inscription_config: 铭文配置
        description: 配置说明
        win_rate: 胜率
    """
    
    # 推荐方案ID
    # int: 整数类型
    # 必填字段，没有默认值
    # 用途: 铭文推荐方案的唯一标识符
    id: int
    
    # 适用段位
    # str: 字符串类型
    # 必填字段，没有默认值
    # 用途: 该铭文方案适用的段位
    rank: str
    
    # 铭文页名称
    # str: 字符串类型
    # 必填字段，没有默认值
    # 用途: 铭文页的自定义名称
    # 示例: "刺客通用"、"射手暴击"
    inscription_name: str
    
    # 铭文配置
    # Dict[str, Any]: 字典类型
    # 必填字段，没有默认值
    # 用途: 铭文的详细配置
    # 示例: {
    #   "red": [{"id": 1, "name": "无双", "count": 10}],
    #   "blue": [{"id": 2, "name": "鹰眼", "count": 10}],
    #   "green": [{"id": 3, "name": "夺萃", "count": 10}]
    # }
    inscription_config: Dict[str, Any]
    
    # 配置说明
    # Optional[str]: 可选的字符串类型，可以为None
    # 用途: 解释该铭文方案的适用场景和效果
    description: Optional[str]
    
    # 胜率
    # float: 浮点数类型
    # 必填字段，没有默认值
    # 用途: 使用该铭文方案的胜率
    win_rate: float
    
    class Config:
        """
        Pydantic配置类
        """
        from_attributes = True


class BPSuggestion(BaseModel):
    """
    BP建议模型
    
    用于返回BP（Ban/Pick）阶段的建议
    
    功能:
        - 提供BP策略建议
        - 包含禁用和选择建议
        - 综合评估和推荐
    
    使用场景:
        - BP阶段智能推荐
        - 英雄选择辅助
        - 对阵分析
    
    字段说明:
        shortcoming: 劣势分析
        ban_suggestions: 禁用建议列表
        counter_recommendations: 克制英雄推荐列表
        overall_rating: 综合评分
    """
    
    # 劣势分析
    # str: 字符串类型
    # 必填字段，没有默认值
    # 用途: 分析当前阵容的劣势
    # 示例: "阵容缺乏控制，前排不足"
    shortcoming: str
    
    # 禁用建议列表
    # List[str]: 字符串列表
    # 必填字段，没有默认值
    # 用途: 建议禁用的英雄名称列表
    # 示例: ["张良", "东皇太一", "妲己"]
    ban_suggestions: List[str]
    
    # 克制英雄推荐列表
    # List[str]: 字符串列表
    # 必填字段，没有默认值
    # 用途: 推荐选择克制敌方阵容的英雄
    # 示例: ["兰陵王", "孙悟空", "铠"]
    counter_recommendations: List[str]
    
    # 综合评分
    # str: 字符串类型
    # 必填字段，没有默认值
    # 用途: 当前阵容的综合评分
    # 示例: "S"、"A"、"B"、"C"、"D"
    overall_rating: str
