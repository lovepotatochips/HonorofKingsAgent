# 导入SQLAlchemy的Column类，用于定义表的列
# Column是ORM中定义字段的基本单位
from sqlalchemy import Column, String, DateTime, JSON, Integer, ForeignKey, Float, Text

# 导入relationship函数，用于定义表之间的关系
# relationship用于建立ORM对象之间的关系（一对多、多对多等）
from sqlalchemy.orm import relationship

# 导入datetime类，用于处理日期时间
from datetime import datetime

# 导入Base基类，所有ORM模型都继承自Base
from app.core.database import Base


class Match(Base):
    """
    对局模型
    
    表示王者荣耀的一场比赛记录
    
    数据库表名: matches
    
    主要功能:
        - 存储对局的基本信息（结果、时长、段位等）
        - 记录玩家的表现数据（击杀、死亡、助攻、伤害等）
        - 存储使用的英雄、装备、铭文等信息
    
    字段说明:
        id: 对局唯一标识符
        user_id: 关联的用户ID
        hero_id: 使用的英雄ID
        hero_name: 使用的英雄名称
        position: 对局位置
        result: 对局结果
        duration: 对局时长（秒）
        kills: 击杀数
        deaths: 死亡数
        assists: 助攻数
        gold: 获得金币
        damage: 造成伤害
        damage_taken: 承受伤害
        healing: 治疗量
        participation_rate: 参团率
        kda: KDA比率
        equipment_list: 装备列表
        inscription: 铭文配置
        rank: 段位
        screenshot_url: 对局截图URL
        created_at: 记录创建时间
    
    关系:
        user: 对局与用户的多对一关系
    """
    
    # ==================== 表定义 ====================
    
    # 指定数据库表名
    # SQL: CREATE TABLE matches (...)
    __tablename__ = "matches"
    
    # ==================== 主键字段 ====================
    
    # 对局ID，主键
    # primary_key=True: 该字段是表的主键，唯一标识一条记录
    # index=True: 为该字段创建索引，加快查询速度
    # String(50): 字符串类型，最大长度50
    id = Column(String(50), primary_key=True, index=True)
    
    # ==================== 关联字段 ====================
    
    # 用户ID，外键关联到users表
    # String(50): 字符串类型，最大长度50
    # ForeignKey("users.id"): 外键，关联到users表的id字段
    # nullable=False: 不能为空，必须指定用户
    # index=True: 创建索引，加快按用户查询对局的速度
    user_id = Column(String(50), ForeignKey("users.id"), nullable=False, index=True)
    
    # ==================== 英雄信息字段 ====================
    
    # 使用的英雄ID
    # Integer: 整数类型
    # ForeignKey("heroes.id"): 外键，关联到heroes表的id字段
    # nullable=True (默认): 可以为空
    # 用途: 记录用户在对局中使用的英雄
    hero_id = Column(Integer, ForeignKey("heroes.id"))
    
    # 使用的英雄名称
    # String(50): 字符串类型，最大长度50
    # 用途: 冗余存储英雄名称，便于查询和显示
    hero_name = Column(String(50))
    
    # 对局位置
    # String(20): 字符串类型，最大长度20
    # 用途: 记录用户在对局中的位置
    # 示例: "top"（上路）、"jungle"（打野）、"mid"（中路）、"archer"（发育路）、"support"（辅助）
    position = Column(String(20))
    
    # ==================== 对局基本信息字段 ====================
    
    # 对局结果
    # String(10): 字符串类型，最大长度10
    # 用途: 记录对局的胜负情况
    # 示例: "victory"（胜利）、"defeat"（失败）、"draw"（平局）
    result = Column(String(10))
    
    # 对局时长（秒）
    # Integer: 整数类型
    # 用途: 记录对局持续的时间，用于分析对局节奏
    # 示例: 1200 表示20分钟
    duration = Column(Integer)
    
    # ==================== 表现数据字段 ====================
    
    # 击杀数
    # Integer: 整数类型，默认值为0
    # default=0: 如果不指定，默认为0
    kills = Column(Integer, default=0)
    
    # 死亡数
    # Integer: 整数类型，默认值为0
    deaths = Column(Integer, default=0)
    
    # 助攻数
    # Integer: 整数类型，默认值为0
    assists = Column(Integer, default=0)
    
    # ==================== 经济和伤害字段 ====================
    
    # 获得金币
    # Integer: 整数类型，默认值为0
    # 用途: 记录玩家在对局中获得的总金币
    gold = Column(Integer, default=0)
    
    # 造成伤害
    # Integer: 整数类型，默认值为0
    # 用途: 记录玩家对敌方英雄造成的总伤害
    damage = Column(Integer, default=0)
    
    # 承受伤害
    # Integer: 整数类型，默认值为0
    # 用途: 记录玩家承受的总伤害
    damage_taken = Column(Integer, default=0)
    
    # 治疗量
    # Integer: 整数类型，默认值为0
    # 用途: 记录玩家对队友的治疗量
    healing = Column(Integer, default=0)
    
    # ==================== 分析数据字段 ====================
    
    # 参团率
    # Float: 浮点数类型，默认值为0.0
    # 用途: 计算公式：（击杀+助攻）/团队总击杀数
    # 示例: 0.7 表示70%的参团率
    participation_rate = Column(Float, default=0.0)
    
    # KDA比率
    # Float: 浮点数类型，默认值为0.0
    # 用途: 计算公式：（击杀+助攻）/最大（死亡，1）
    # 示例: 5.0 表示平均每次死亡造成5个击杀或助攻
    kda = Column(Float, default=0.0)
    
    # ==================== 配置字段 ====================
    
    # 装备列表
    # JSON: JSON类型，可以存储复杂的数据结构
    # 用途: 存储玩家在对局中购买的装备
    # 示例: [
    #   {"id": 1, "name": "无尽战刃", "order": 1},
    #   {"id": 2, "name": "影刃", "order": 2}
    # ]
    equipment_list = Column(JSON)
    
    # 铭文配置
    # JSON: JSON类型，可以存储复杂的数据结构
    # 用途: 存储玩家使用的铭文页配置
    # 示例: {
    #   "red": [{"id": 1, "name": "无双", "count": 10}],
    #   "blue": [{"id": 2, "name": "鹰眼", "count": 10}],
    #   "green": [{"id": 3, "name": "夺萃", "count": 10}]
    # }
    inscription = Column(JSON)
    
    # ==================== 其他信息字段 ====================
    
    # 段位
    # String(50): 字符串类型，最大长度50
    # 用途: 记录对局时的段位
    # 示例: "钻石II"、"星耀III"
    rank = Column(String(50))
    
    # 对局截图URL
    # String(200): 字符串类型，最大长度200
    # 用途: 存储对局结束后的截图，用于回顾和分析
    screenshot_url = Column(String(200))
    
    # ==================== 时间戳字段 ====================
    
    # 记录创建时间
    # DateTime: 日期时间类型
    # default=datetime.utcnow: 默认值为当前UTC时间
    # 用途: 记录对局记录的创建时间，用于排序
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # ==================== 关系定义 ====================
    
    # 对局与用户的多对一关系
    # 多场对局记录属于一个用户
    # relationship: 定义ORM关系
    # "User": 关联的模型类名
    # back_populates="matches": 指向User模型中名为"matches"的反向关系
    user = relationship("User", back_populates="matches")


class Analysis(Base):
    """
    对局分析模型
    
    表示对局的AI分析报告
    
    数据库表名: analyses
    
    主要功能:
        - 存储对局的AI分析结果
        - 记录高光时刻和失误点
        - 提供改进建议和详细报告
    
    字段说明:
        id: 分析报告唯一标识符
        match_id: 关联的对局ID
        overall_rating: 整体评分
        highlights: 高光时刻列表
        mistakes: 失误列表
        suggestions: 建议列表
        report: 详细分析报告
        improvements: 改进建议
        created_at: 分析创建时间
    """
    
    # ==================== 表定义 ====================
    
    # 指定数据库表名
    # SQL: CREATE TABLE analyses (...)
    __tablename__ = "analyses"
    
    # ==================== 主键字段 ====================
    
    # 分析报告ID，主键
    # primary_key=True: 该字段是表的主键，唯一标识一条记录
    # index=True: 为该字段创建索引，加快查询速度
    # String(50): 字符串类型，最大长度50
    id = Column(String(50), primary_key=True, index=True)
    
    # ==================== 关联字段 ====================
    
    # 对局ID，外键关联到matches表
    # String(50): 字符串类型，最大长度50
    # ForeignKey("matches.id"): 外键，关联到matches表的id字段
    # nullable=False: 不能为空，必须指定对局
    # index=True: 创建索引，加快按对局查询分析的速度
    match_id = Column(String(50), ForeignKey("matches.id"), nullable=False, index=True)
    
    # ==================== 评分字段 ====================
    
    # 整体评分
    # String(20): 字符串类型，最大长度20
    # 用途: AI给出的整体评分
    # 示例: "S"、"A"、"B"、"C"、"D"
    overall_rating = Column(String(20))
    
    # ==================== 分析内容字段 ====================
    
    # 高光时刻列表
    # JSON: JSON类型，可以存储复杂的数据结构
    # 用途: 记录对局中的精彩表现
    # 示例: [
    #   {
    #     "time": "5:30",
    #     "description": "成功击杀敌方C位",
    #     "impact": "high"
    #   },
    #   {
    #     "time": "12:15",
    #     "description": "五连绝世",
    #     "impact": "very_high"
    #   }
    # ]
    highlights = Column(JSON)
    
    # 失误列表
    # JSON: JSON类型，可以存储复杂的数据结构
    # 用途: 记录对局中的失误和需要改进的地方
    # 示例: [
    #   {
    #     "time": "8:20",
    #     "description": "单带过深被Gank",
    #     "severity": "medium",
    #     "suggestion": "注意地图信息，避免单带"
    #   }
    # ]
    mistakes = Column(JSON)
    
    # 建议列表
    # JSON: JSON类型，可以存储复杂的数据结构
    # 用途: 提供改进建议
    # 示例: [
    #   {
    #     "category": "positioning",
    #     "suggestion": "团战时保持安全距离",
    #     "priority": "high"
    #   },
    #   {
    #     "category": "timing",
    #     "suggestion": "把握团战进场时机",
    #     "priority": "medium"
    #   }
    # ]
    suggestions = Column(JSON)
    
    # ==================== 报告字段 ====================
    
    # 详细分析报告
    # Text: 文本类型，可以存储大量文本
    # 用途: AI生成的详细文字报告
    # 示例: "本局表现优秀，KDA达到5.0。高光时刻包括5:30的精彩击杀和12:15的五连绝世。需要注意8:20的单带过深问题，建议团战时保持安全距离..."
    report = Column(Text)
    
    # 改进建议
    # JSON: JSON类型，可以存储复杂的数据结构
    # 用途: 长期改进建议和训练计划
    # 示例: {
    #   "short_term": [
    #     "练习团战站位",
    #     "提高地图意识"
    #   ],
    #   "long_term": [
    #     "加强英雄熟练度",
    #     "学习职业选手操作"
    #   ]
    # }
    improvements = Column(JSON)
    
    # ==================== 时间戳字段 ====================
    
    # 分析创建时间
    # DateTime: 日期时间类型
    # default=datetime.utcnow: 默认值为当前UTC时间
    # 用途: 记录分析报告的创建时间
    created_at = Column(DateTime, default=datetime.utcnow)
