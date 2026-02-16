# 导入类型提示
# List: 列表类型
# Optional: 可选类型（可以为None）
from typing import List, Optional

# 导入Session类
# Session: SQLAlchemy的数据库会话，用于与数据库交互
from sqlalchemy.orm import Session

# 导入英雄相关的模型
# Hero: 英雄模型
# HeroEquipment: 英雄装备模型
# HeroInscription: 英雄铭文模型
from app.models.hero import Hero, HeroEquipment, HeroInscription

# 导入英雄相关的Schema
# HeroResponse: 英雄响应模型
# HeroDetailResponse: 英雄详情响应模型
# EquipmentResponse: 装备响应模型
# BPSuggestion: BP建议模型
from app.schemas.hero import HeroResponse, HeroDetailResponse, EquipmentResponse, BPSuggestion


class HeroService:
    """
    英雄服务类
    
    负责处理英雄相关的业务逻辑
    
    主要功能:
        - 英雄列表查询
        - 英雄详情查询
        - 英雄装备推荐
        - 英雄铭文推荐
        - BP（Ban/Pick）建议
    
    设计模式:
        - 服务层模式（Service Layer）
        - 将业务逻辑与数据访问分离
        - 提供清晰的API供控制器调用
    
    使用场景:
        - 英雄浏览和查询
        - 英雄详情展示
        - 装备和铭文推荐
        - BP阶段的建议
    """
    
    def get_hero_list(
        self,
        position: Optional[str],
        difficulty: Optional[str],
        search: Optional[str],
        db: Session
    ) -> List[HeroResponse]:
        """
        获取英雄列表
        
        参数:
            position: 英雄位置过滤（如"射手"、"法师"等）
            difficulty: 难度过滤（如"简单"、"困难"等）
            search: 搜索关键词（英雄名称）
            db: 数据库会话对象
        
        返回:
            List[HeroResponse]: 英雄列表
        
        功能:
            - 查询英雄列表
            - 支持按位置过滤
            - 支持按难度过滤
            - 支持关键词搜索
        
        业务逻辑:
            1. 构建基础查询
            2. 如果指定了位置，添加位置过滤条件
            3. 如果指定了难度，添加难度过滤条件
            4. 如果指定了搜索关键词，添加搜索条件
            5. 执行查询获取英雄列表
            6. 转换为响应模型列表
        """
        # 构建基础查询
        # 从Hero表查询所有英雄
        query = db.query(Hero)
        
        # 如果指定了位置，添加位置过滤条件
        if position:
            query = query.filter(Hero.position == position)
        
        # 如果指定了难度，添加难度过滤条件
        if difficulty:
            query = query.filter(Hero.difficulty == difficulty)
        
        # 如果指定了搜索关键词，添加搜索条件
        # contains: 包含指定字符串的模糊匹配
        if search:
            query = query.filter(Hero.name.contains(search))
        
        # 执行查询获取所有匹配的英雄
        heroes = query.all()
        
        # 将数据库模型转换为响应模型列表
        # 使用列表推导式，简洁高效
        return [
            HeroResponse(
                id=hero.id,
                name=hero.name,
                title=hero.title,
                position=hero.position,
                difficulty=hero.difficulty,
                image_url=hero.image_url,
                win_rate=hero.win_rate,
                pick_rate=hero.pick_rate,
                ban_rate=hero.ban_rate
            )
            for hero in heroes
        ]
    
    def get_hero_detail(self, hero_id: int, db: Session) -> Optional[HeroDetailResponse]:
        """
        获取英雄详情
        
        参数:
            hero_id: 英雄ID
            db: 数据库会话对象
        
        返回:
            Optional[HeroDetailResponse]: 英雄详情对象，如果英雄不存在则返回None
        
        功能:
            - 查询英雄的详细信息
            - 包含技能、克制关系等信息
        
        业务逻辑:
            1. 根据hero_id查询英雄
            2. 如果英雄不存在，返回None
            3. 如果英雄存在，返回英雄详情对象
        """
        # 从数据库查询英雄
        # filter: 添加查询条件（英雄ID等于指定值）
        # first(): 获取第一条记录，如果没有则返回None
        hero = db.query(Hero).filter(Hero.id == hero_id).first()
        
        # 如果英雄不存在，返回None
        if not hero:
            return None
        
        # 英雄存在，返回英雄详情对象
        return HeroDetailResponse(
            id=hero.id,
            name=hero.name,
            title=hero.title,
            position=hero.position,
            difficulty=hero.difficulty,
            description=hero.description,
            image_url=hero.image_url,
            skills=hero.skills or [],
            passive_skill=hero.passive_skill,
            win_rate=hero.win_rate,
            pick_rate=hero.pick_rate,
            ban_rate=hero.ban_rate,
            counter_heroes=hero.counter_heroes,
            countered_by_heroes=hero.countered_by_heroes
        )
    
    def get_hero_equipment(
        self,
        hero_id: int,
        rank: str,
        db: Session
    ) -> List[EquipmentResponse]:
        """
        获取英雄装备推荐
        
        参数:
            hero_id: 英雄ID
            rank: 段位（如"黄金"、"钻石"等）
            db: 数据库会话对象
        
        返回:
            List[EquipmentResponse]: 装备推荐列表
        
        功能:
            - 查询英雄的装备推荐
            - 支持按段位过滤
            - 提供不同位置的出装建议
        
        业务逻辑:
            1. 构建基础查询
            2. 如果指定了段位且不是"全部"，添加段位过滤条件
            3. 执行查询获取装备列表
            4. 转换为响应模型列表
        """
        # 构建基础查询
        # 从HeroEquipment表查询该英雄的装备
        query = db.query(HeroEquipment).filter(HeroEquipment.hero_id == hero_id)
        
        # 如果指定了段位且不是"全部"，添加段位过滤条件
        if rank and rank != "全部":
            query = query.filter(HeroEquipment.rank == rank)
        
        # 执行查询获取所有匹配的装备
        equipments = query.all()
        
        # 将数据库模型转换为响应模型列表
        return [
            EquipmentResponse(
                id=eq.id,
                rank=eq.rank,
                position=eq.position,
                equipment_list=eq.equipment_list or [],
                win_rate=eq.win_rate,
                pick_rate=eq.pick_rate
            )
            for eq in equipments
        ]
    
    def get_hero_inscription(
        self,
        hero_id: int,
        rank: str,
        db: Session
    ) -> dict:
        """
        获取英雄铭文推荐
        
        参数:
            hero_id: 英雄ID
            rank: 段位（如"黄金"、"钻石"等）
            db: 数据库会话对象
        
        返回:
            dict: 铭文推荐数据
        
        功能:
            - 查询英雄的铭文推荐
            - 支持按段位过滤
            - 返回铭文配置和描述
        
        业务逻辑:
            1. 构建基础查询
            2. 如果指定了段位且不是"全部"，添加段位过滤条件
            3. 执行查询获取铭文列表
            4. 转换为字典格式返回
        """
        # 构建基础查询
        # 从HeroInscription表查询该英雄的铭文
        query = db.query(HeroInscription).filter(HeroInscription.hero_id == hero_id)
        
        # 如果指定了段位且不是"全部"，添加段位过滤条件
        if rank and rank != "全部":
            query = query.filter(HeroInscription.rank == rank)
        
        # 执行查询获取所有匹配的铭文
        inscriptions = query.all()
        
        # 转换为字典格式返回
        return {
            # 英雄ID
            "hero_id": hero_id,
            # 段位
            "rank": rank,
            # 铭文列表
            "inscriptions": [
                {
                    "id": ins.id,
                    "rank": ins.rank,
                    "inscription_name": ins.inscription_name,
                    "inscription_config": ins.inscription_config,
                    "description": ins.description,
                    "win_rate": ins.win_rate
                }
                for ins in inscriptions
            ]
        }
    
    def get_bp_suggestion(
        self,
        our_heroes: List[str],
        enemy_heroes: List[str],
        db: Session
    ) -> BPSuggestion:
        """
        获取BP（Ban/Pick）建议
        
        参数:
            our_heroes: 我方英雄列表
            enemy_heroes: 敌方英雄列表
            db: 数据库会话对象
        
        返回:
            BPSuggestion: BP建议对象
        
        功能:
            - 分析阵容短板
            - 生成禁选建议
            - 提供counter英雄推荐
            - 评估整体阵容优势
        
        业务逻辑:
            1. 分析我方阵容的短板
            2. 根据敌方英雄生成禁选建议
            3. 提供counter英雄推荐
            4. 评估整体阵容优势
            5. 返回BP建议
        
        BP阶段:
            - Ban阶段：禁选英雄
            - Pick阶段：选择英雄
            - 目标：优化阵容，提高胜率
        """
        # 分析我方阵容的短板
        shortcomings = self._analyze_shortcomings(our_heroes, db)
        
        # 生成禁选建议
        ban_suggestions = self._generate_ban_suggestions(enemy_heroes, db)
        
        # 获取counter英雄推荐
        counter_recommendations = self._get_counter_recommendations(our_heroes, enemy_heroes, db)
        
        # 评估整体阵容优势
        overall_rating = self._evaluate_overall_rating(our_heroes, enemy_heroes, db)
        
        # 返回BP建议对象
        return BPSuggestion(
            shortcoming=shortcomings,
            ban_suggestions=ban_suggestions,
            counter_recommendations=counter_recommendations,
            overall_rating=overall_rating
        )
    
    def _analyze_shortcomings(self, heroes: List[str], db: Session) -> str:
        """
        分析阵容短板
        
        参数:
            heroes: 英雄名称列表
            db: 数据库会话对象
        
        返回:
            str: 阵容短板描述
        
        功能:
            - 分析阵容缺少的位置
            - 提供阵容优化建议
        
        业务逻辑:
            1. 遍历英雄列表，收集所有位置
            2. 比较必需位置和实际位置
            3. 找出缺少的位置
            4. 返回短板描述
        
        私有方法:
            - 以下划线开头，表示内部方法
            - 只在类内部使用，不对外暴露
        
        必需位置:
            - tank: 坦克
            - support: 辅助
            - mage: 法师
            - archer: 射手
        """
        # 初始化位置集合
        positions = set()
        
        # 遍历英雄列表
        for hero_name in heroes:
            # 查询英雄信息
            hero = db.query(Hero).filter(Hero.name == hero_name).first()
            
            # 如果英雄存在，添加其位置
            if hero:
                positions.add(hero.position)
        
        # 计算缺少的位置
        # 必需位置集合减去实际位置集合
        missing_positions = {"tank", "support", "mage", "archer"} - positions
        
        # 如果有缺少的位置，返回短板描述
        if missing_positions:
            return f"阵容缺少{', '.join(missing_positions)}位置"
        
        # 阵容完整
        return "阵容结构较为完整"
    
    def _generate_ban_suggestions(self, enemy_heroes: List[str], db: Session) -> List[str]:
        """
        生成禁选建议
        
        参数:
            enemy_heroes: 敌方英雄列表
            db: 数据库会话对象
        
        返回:
            List[str]: 禁选建议列表
        
        功能:
            - 根据敌方英雄生成禁选建议
            - 优先禁选高禁用率的英雄
        
        业务逻辑:
            1. 遍历敌方英雄列表
            2. 查询英雄的禁用率
            3. 如果禁用率超过30%，建议禁选
            4. 返回禁选建议列表
        
        私有方法:
            - 以下划线开头，表示内部方法
            - 只在类内部使用，不对外暴露
        
        禁选策略:
            - 优先禁选高禁用率英雄
            - 避免敌方拿到强势英雄
        """
        # 初始化建议列表
        suggestions = []
        
        # 遍历敌方英雄列表
        for hero_name in enemy_heroes:
            # 查询英雄信息
            hero = db.query(Hero).filter(Hero.name == hero_name).first()
            
            # 如果英雄存在且禁用率超过30%，建议禁选
            if hero and hero.ban_rate > 0.3:
                suggestions.append(f"{hero_name}（禁用率{hero.ban_rate*100:.1f}%）")
        
        # 如果有建议，返回建议列表
        # 否则返回默认建议
        return suggestions if suggestions else ["根据版本选择禁用"]
    
    def _get_counter_recommendations(
        self,
        our_heroes: List[str],
        enemy_heroes: List[str],
        db: Session
    ) -> List[str]:
        """
        获取counter英雄推荐
        
        参数:
            our_heroes: 我方英雄列表
            enemy_heroes: 敌方英雄列表
            db: 数据库会话对象
        
        返回:
            List[str]: counter英雄推荐列表
        
        功能:
            - 针对敌方英雄推荐counter英雄
            - 帮助玩家选择克制英雄
        
        业务逻辑:
            1. 遍历敌方英雄列表
            2. 查询每个英雄的counter英雄
            3. 生成推荐列表
            4. 返回counter英雄推荐
        
        私有方法:
            - 以下划线开头，表示内部方法
            - 只在类内部使用，不对外暴露
        
        Counter策略:
            - 选择克制敌方英雄的角色
            - 提高对线优势
        """
        # 初始化推荐列表
        recommendations = []
        
        # 遍历敌方英雄列表
        for hero_name in enemy_heroes:
            # 查询英雄信息
            hero = db.query(Hero).filter(Hero.name == hero_name).first()
            
            # 如果英雄存在且有counter英雄信息
            if hero and hero.countered_by_heroes:
                # 添加counter推荐，最多显示前3个
                recommendations.append(f"counter {hero_name}: {', '.join(hero.countered_by_heroes[:3])}")
        
        # 如果有推荐，返回推荐列表
        # 否则返回默认推荐
        return recommendations if recommendations else ["根据对位选择counter英雄"]
    
    def _evaluate_overall_rating(
        self,
        our_heroes: List[str],
        enemy_heroes: List[str],
        db: Session
    ) -> str:
        """
        评估整体阵容优势
        
        参数:
            our_heroes: 我方英雄列表
            enemy_heroes: 敌方英雄列表
            db: 数据库会话对象
        
        返回:
            str: 阵容优势评价（"优势"、"劣势"、"均势"）
        
        功能:
            - 比较双方阵容的整体实力
            - 基于英雄胜率进行评估
        
        业务逻辑:
            1. 计算我方英雄的平均胜率
            2. 计算敌方英雄的平均胜率
            3. 比较双方胜率
            4. 返回阵容优势评价
        
        私有方法:
            - 以下划线开头，表示内部方法
            - 只在类内部使用，不对外暴露
        
        评估标准:
            - 我方胜率 > 敌方胜率: 优势
            - 我方胜率 < 敌方胜率: 劣势
            - 我方胜率 = 敌方胜率: 均势
        """
        # 初始化双方胜率
        our_win_rate = 0
        enemy_win_rate = 0
        
        # 计算我方英雄的总胜率
        for hero_name in our_heroes:
            hero = db.query(Hero).filter(Hero.name == hero_name).first()
            if hero:
                our_win_rate += hero.win_rate
        
        # 计算敌方英雄的总胜率
        for hero_name in enemy_heroes:
            hero = db.query(Hero).filter(Hero.name == hero_name).first()
            if hero:
                enemy_win_rate += hero.win_rate
        
        # 比较双方胜率，返回阵容优势评价
        if our_win_rate > enemy_win_rate:
            return "优势"
        elif our_win_rate < enemy_win_rate:
            return "劣势"
        else:
            return "均势"
