# 导入SQLAlchemy的Column类，用于定义表的列
# Column是ORM中定义字段的基本单位
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, JSON, ForeignKey

# 导入relationship函数，用于定义表之间的关系
# relationship用于建立ORM对象之间的关系（一对多、多对多等）
from sqlalchemy.orm import relationship

# 导入datetime类，用于处理日期时间
from datetime import datetime

# 导入Base基类，所有ORM模型都继承自Base
from app.core.database import Base


class Hero(Base):
    """
    英雄模型
    
    表示王者荣耀游戏中的英雄角色
    
    数据库表名: heroes
    
    主要功能:
        - 存储英雄的基本信息（名称、位置、难度等）
        - 记录英雄的技能信息（主动技能、被动技能）
        - 存储英雄的胜率、ban率、pick率等统计数据
        - 管理英雄的克制关系
    
    字段说明:
        id: 英雄唯一标识符
        name: 英雄名称
        title: 英雄称号
        position: 英雄定位
        difficulty: 难度等级
        description: 英雄描述
        image_url: 英雄图片URL
        skills: 主动技能列表
        passive_skill: 被动技能
        win_rate: 胜率
        ban_rate: 禁用率
        pick_rate: 选用率
        counter_heroes: 克制的英雄列表
        countered_by_heroes: 被克制的英雄列表
        version: 游戏版本
        created_at: 创建时间
        updated_at: 更新时间
    
    关系:
        equipments: 英雄与装备推荐的一对多关系
        inscriptions: 英雄与铭文推荐的一对多关系
    """
    
    # ==================== 表定义 ====================
    
    # 指定数据库表名
    # SQL: CREATE TABLE heroes (...)
    __tablename__ = "heroes"
    
    # ==================== 主键字段 ====================
    
    # 英雄ID，主键
    # primary_key=True: 该字段是表的主键，唯一标识一条记录
    # index=True: 为该字段创建索引，加快查询速度
    # Integer: 整数类型，自增主键
    id = Column(Integer, primary_key=True, index=True)
    
    # ==================== 基本信息 ====================
    
    # 英雄名称
    # String(50): 字符串类型，最大长度50
    # unique=True: 名称必须唯一，不能有重复的英雄名称
    # index=True: 创建索引，加快按名称查询英雄的速度
    # nullable=False: 不能为空，必须有英雄名称
    name = Column(String(50), unique=True, index=True, nullable=False)
    
    # 英雄称号
    # String(100): 字符串类型，最大长度100
    # 用途: 英雄的官方称号
    # 示例: "无敌剑圣"、"暗影刺客"
    title = Column(String(100))
    
    # 英雄定位
    # String(20): 字符串类型，最大长度20
    # 用途: 英雄在游戏中的主要定位
    # 示例: "tank"（坦克）、"warrior"（战士）、"mage"（法师）、"archer"（射手）、"support"（辅助）
    position = Column(String(20))
    
    # 难度等级
    # String(20): 字符串类型，最大长度20
    # 用途: 英雄的操作难度等级
    # 示例: "简单"、"普通"、"困难"、"超难"
    difficulty = Column(String(20))
    
    # 英雄描述
    # Text: 文本类型，可以存储大量文本
    # 用途: 英雄的背景故事、玩法介绍等
    description = Column(Text)
    
    # 英雄图片URL
    # String(500): 字符串类型，最大长度500
    # 用途: 英雄的头像、立绘等图片链接
    image_url = Column(String(500))
    
    # ==================== 技能信息 ====================
    
    # 主动技能列表
    # JSON: JSON类型，可以存储复杂的数据结构
    # 用途: 存储英雄的主动技能信息
    # 示例: [
    #   {
    #     "id": 1,
    #     "name": "秘术·影",
    #     "type": "主动",
    #     "description": "冷却值：0 消耗：0 兰陵王向指定方向位移...",
    #     "cooldown": "0",
    #     "cost": "0"
    #   },
    #   {
    #     "id": 2,
    #     "name": "影刃",
    #     "type": "主动",
    #     "description": "冷却值：8 消耗：50 兰陵王朝指定方向掷出匕首...",
    #     "cooldown": "8",
    #     "cost": "50"
    #   }
    # ]
    skills = Column(JSON)
    
    # 被动技能
    # JSON: JSON类型，可以存储复杂的数据结构
    # 用途: 存储英雄的被动技能信息
    # 示例: {
    #   "id": 0,
    #   "name": "暗影",
    #   "type": "被动",
    #   "description": "兰陵王在敌方视野外时...",
    #   "cooldown": null,
    #   "cost": null
    # }
    passive_skill = Column(JSON)
    
    # ==================== 统计数据 ====================
    
    # 胜率
    # Float: 浮点数类型，默认值为0.0
    # 用途: 英雄的对局胜率，单位为百分比
    # 示例: 0.52 表示52%的胜率
    win_rate = Column(Float, default=0.0)
    
    # 禁用率
    # Float: 浮点数类型，默认值为0.0
    # 用途: 英雄在BP阶段的禁用率，单位为百分比
    # 示例: 0.15 表示15%的禁用率
    ban_rate = Column(Float, default=0.0)
    
    # 选用率
    # Float: 浮点数类型，默认值为0.0
    # 用途: 英雄在BP阶段的选用率，单位为百分比
    # 示例: 0.35 表示35%的选用率
    pick_rate = Column(Float, default=0.0)
    
    # ==================== 克制关系 ====================
    
    # 克制的英雄列表
    # JSON: JSON类型，可以存储复杂的数据结构
    # 用途: 记录该英雄克制的其他英雄
    # 示例: [
    #   {"id": 1, "name": "鲁班七号", "reason": "高爆发秒杀"},
    #   {"id": 2, "name": "后羿", "reason": "位移克制"}
    # ]
    counter_heroes = Column(JSON)
    
    # 被克制的英雄列表
    # JSON: JSON类型，可以存储复杂的数据结构
    # 用途: 记录克制该英雄的其他英雄
    # 示例: [
    #   {"id": 3, "name": "张良", "reason": "压制位移"},
    #   {"id": 4, "name": "东皇太一", "reason": "大招压制"}
    # ]
    countered_by_heroes = Column(JSON)
    
    # ==================== 版本信息 ====================
    
    # 游戏版本
    # String(20): 字符串类型，最大长度20
    # 用途: 记录英雄数据的游戏版本
    # 示例: "1.50.1.8"
    version = Column(String(20))
    
    # ==================== 时间戳 ====================
    
    # 创建时间
    # DateTime: 日期时间类型
    # default=datetime.utcnow: 默认值为当前UTC时间
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 更新时间
    # DateTime: 日期时间类型
    # default=datetime.utcnow: 默认值为当前UTC时间
    # onupdate=datetime.utcnow: 每次更新记录时自动设置为当前时间
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # ==================== 关系定义 ====================
    
    # 英雄与装备推荐的一对多关系
    # 一个英雄可以有多种装备推荐方案
    equipments = relationship("HeroEquipment", back_populates="hero", cascade="all, delete-orphan")
    
    # 英雄与铭文推荐的一对多关系
    # 一个英雄可以有多种铭文推荐方案
    inscriptions = relationship("HeroInscription", back_populates="hero", cascade="all, delete-orphan")


class HeroEquipment(Base):
    """
    英雄装备推荐模型
    
    表示英雄的装备推荐方案
    
    数据库表名: hero_equipments
    
    主要功能:
        - 存储英雄的装备推荐方案
        - 记录不同段位、不同位置的装备搭配
        - 提供装备方案的统计数据
    
    字段说明:
        id: 推荐方案唯一标识符
        hero_id: 关联的英雄ID
        rank: 适用段位
        position: 适用位置
        equipment_list: 装备列表
        win_rate: 胜率
        pick_rate: 选用率
        version: 游戏版本
        created_at: 创建时间
    
    关系:
        hero: 装备推荐与英雄的多对一关系
    """
    
    # 指定数据库表名
    __tablename__ = "hero_equipments"
    
    # 主键
    id = Column(Integer, primary_key=True, index=True)
    
    # 关联的英雄ID
    hero_id = Column(Integer, ForeignKey("heroes.id"), nullable=False)
    
    # 适用段位
    # String(20): 字符串类型，最大长度20
    # 用途: 该装备方案适用的段位
    # 示例: "青铜"、"黄金"、"钻石"、"星耀"、"王者"
    rank = Column(String(20))
    
    # 适用位置
    # String(20): 字符串类型，最大长度20
    # 用途: 该装备方案适用的位置
    # 示例: "top"（上路）、"jungle"（打野）、"mid"（中路）、"archer"（发育路）、"support"（辅助）
    position = Column(String(20))
    
    # 装备列表
    # JSON: JSON类型，存储装备推荐
    # 示例: [
    #   {"id": 1, "name": "暗影战斧", "order": 1},
    #   {"id": 2, "name": "抵抗之靴", "order": 2},
    #   {"id": 3, "name": "无尽战刃", "order": 3}
    # ]
    equipment_list = Column(JSON)
    
    # 胜率
    # Float: 浮点数类型
    # 用途: 使用该装备方案的胜率
    win_rate = Column(Float)
    
    # 选用率
    # Float: 浮点数类型
    # 用途: 该装备方案的使用频率
    pick_rate = Column(Float)
    
    # 游戏版本
    version = Column(String(20))
    
    # 创建时间
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    hero = relationship("Hero", back_populates="equipments")


class HeroInscription(Base):
    """
    英雄铭文推荐模型
    
    表示英雄的铭文推荐方案
    
    数据库表名: hero_inscriptions
    
    主要功能:
        - 存储英雄的铭文推荐方案
        - 记录不同段位的铭文搭配
        - 提供铭文方案的统计数据
    
    字段说明:
        id: 推荐方案唯一标识符
        hero_id: 关联的英雄ID
        rank: 适用段位
        inscription_name: 铭文页名称
        inscription_config: 铭文配置
        description: 配置说明
        win_rate: 胜率
        version: 游戏版本
        created_at: 创建时间
    
    关系:
        hero: 铭文推荐与英雄的多对一关系
    """
    
    # 指定数据库表名
    __tablename__ = "hero_inscriptions"
    
    # 主键
    id = Column(Integer, primary_key=True, index=True)
    
    # 关联的英雄ID
    hero_id = Column(Integer, ForeignKey("heroes.id"), nullable=False)
    
    # 适用段位
    rank = Column(String(20))
    
    # 铭文页名称
    # String(50): 字符串类型，最大长度50
    # 用途: 铭文页的自定义名称
    # 示例: "刺客通用"、"射手暴击"
    inscription_name = Column(String(50))
    
    # 铭文配置
    # JSON: JSON类型，存储铭文详情
    # 示例: {
    #   "red": [{"id": 1, "name": "无双", "count": 10}],
    #   "blue": [{"id": 2, "name": "鹰眼", "count": 10}],
    #   "green": [{"id": 3, "name": "夺萃", "count": 10}]
    # }
    inscription_config = Column(JSON)
    
    # 配置说明
    # Text: 文本类型
    # 用途: 解释该铭文方案的适用场景和效果
    description = Column(Text)
    
    # 胜率
    win_rate = Column(Float)
    
    # 游戏版本
    version = Column(String(20))
    
    # 创建时间
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    hero = relationship("Hero", back_populates="inscriptions")


class Equipment(Base):
    """
    装备模型
    
    表示王者荣耀游戏中的装备
    
    数据库表名: equipments
    
    主要功能:
        - 存储装备的基本信息（名称、类型、价格等）
        - 记录装备的属性和技能效果
        - 管理装备的合成关系
    
    字段说明:
        id: 装备唯一标识符
        name: 装备名称
        type: 装备类型
        price: 装备价格
        stats: 装备属性
        passive: 被动技能描述
        active: 主动技能描述
        build_from: 合成来源
        build_into: 可合成的装备
        version: 游戏版本
        created_at: 创建时间
        updated_at: 更新时间
    """
    
    # 指定数据库表名
    __tablename__ = "equipments"
    
    # 主键
    id = Column(Integer, primary_key=True, index=True)
    
    # 装备名称
    # unique=True: 名称必须唯一
    name = Column(String(50), unique=True, index=True, nullable=False)
    
    # 装备类型
    # String(20): 字符串类型，最大长度20
    # 用途: 装备的分类
    # 示例: "attack"（攻击）、"defense"（防御）、"move"（移动）、"magic"（法术）
    type = Column(String(20))
    
    # 装备价格
    # Integer: 整数类型
    # 用途: 装备的购买价格（金币）
    price = Column(Integer)
    
    # 装备属性
    # JSON: JSON类型，存储装备提供的属性
    # 示例: {
    #   "attack_power": 120,
    #   "attack_speed": 20,
    #   "critical_chance": 20
    # }
    stats = Column(JSON)
    
    # 被动技能描述
    # Text: 文本类型
    # 用途: 装备的被动技能效果说明
    passive = Column(Text)
    
    # 主动技能描述
    # Text: 文本类型
    # 用途: 装备的主动技能效果说明（如果有）
    active = Column(Text)
    
    # 合成来源
    # JSON: JSON类型，存储合成该装备所需的小件
    # 示例: [
    #   {"id": 1, "name": "风暴巨剑", "price": 910},
    #   {"id": 2, "name": "匕首", "price": 290}
    # ]
    build_from = Column(JSON)
    
    # 可合成的装备
    # JSON: JSON类型，存储可以用该装备合成的大件
    # 示例: [
    #   {"id": 10, "name": "无尽战刃"},
    #   {"id": 11, "name": "影刃"}
    # ]
    build_into = Column(JSON)
    
    # 游戏版本
    version = Column(String(20))
    
    # 创建时间
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 更新时间
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
