# 导入类型提示
# List: 列表类型
from typing import List

# 导入Session类
# Session: SQLAlchemy的数据库会话，用于与数据库交互
from sqlalchemy.orm import Session

# 导入对局模型
# Match: 对局数据库模型
from app.models.match import Match

# 导入对局相关的Schema
# MatchData: 对局数据模型
# MatchSummary: 对局摘要模型
from app.schemas.match import MatchData, MatchSummary

# 导入uuid模块
# uuid: 用于生成唯一标识符
import uuid


class MatchService:
    """
    对局服务类
    
    负责处理对局相关的业务逻辑
    
    主要功能:
        - 导入对局数据
        - 查询对局历史
        - 获取对局摘要
        - 删除对局记录
    
    设计模式:
        - 服务层模式（Service Layer）
        - 将业务逻辑与数据访问分离
        - 提供清晰的API供控制器调用
    
    使用场景:
        - 对局数据导入
        - 对局历史查看
        - 对局详情查看
        - 对局记录删除
    """
    
    async def import_match(self, match_data: MatchData, db: Session) -> dict:
        """
        导入对局数据
        
        参数:
            match_data: 对局数据
            db: 数据库会话对象
        
        返回:
            dict: 导入结果，包含对局ID和消息
        
        功能:
            - 导入对局数据到数据库
            - 生成对局ID
            - 保存对局信息
        
        业务逻辑:
            1. 生成唯一的对局ID
            2. 创建对局模型实例
            3. 设置对局数据
            4. 保存到数据库
            5. 返回导入结果
        
        异步处理:
            - async: 异步方法，不阻塞主线程
        
        对局数据包含:
            - 用户信息
            - 英雄信息
            - 对局结果
            - 统计数据（KDA、参团率等）
            - 装备和铭文
        """
        # 生成唯一的对局ID
        # 使用uuid4生成随机UUID
        match_id = str(uuid.uuid4())
        
        # 创建对局模型实例
        match = Match(
            # 对局ID
            id=match_id,
            # 用户ID
            user_id=match_data.user_id,
            # 英雄ID
            hero_id=match_data.hero_id,
            # 英雄名称
            hero_name=match_data.hero_name,
            # 位置
            position=match_data.position,
            # 对局结果（胜利/失败）
            result=match_data.result,
            # 对局时长（秒）
            duration=match_data.duration,
            # 击杀数
            kills=match_data.kills or 0,
            # 死亡数
            deaths=match_data.deaths or 0,
            # 助攻数
            assists=match_data.assists or 0,
            # 经济
            gold=match_data.gold or 0,
            # 输出伤害
            damage=match_data.damage or 0,
            # 承受伤害
            damage_taken=match_data.damage_taken or 0,
            # 治疗量
            healing=match_data.healing or 0,
            # 参团率
            participation_rate=match_data.participation_rate or 0.0,
            # KDA比率
            kda=match_data.kda or 0.0,
            # 装备列表
            equipment_list=match_data.equipment_list,
            # 铭文配置
            inscription=match_data.inscription,
            # 段位
            rank=match_data.rank,
            # 截图URL
            screenshot_url=match_data.screenshot_url
        )
        
        # 将对局记录添加到数据库会话
        db.add(match)
        # 提交事务，保存对局记录
        db.commit()
        
        # 返回导入结果
        return {
            # 对局ID
            "match_id": match_id,
            # 成功消息
            "message": "对局数据导入成功"
        }
    
    def get_history(self, user_id: str, limit: int, db: Session) -> List[MatchSummary]:
        """
        获取对局历史
        
        参数:
            user_id: 用户ID
            limit: 返回的记录数量限制
            db: 数据库会话对象
        
        返回:
            List[MatchSummary]: 对局历史列表
        
        功能:
            - 查询用户的对局历史
            - 按时间倒序排列
            - 限制返回的记录数量
        
        业务逻辑:
            1. 根据用户ID查询对局记录
            2. 按创建时间倒序排列（最新的在前）
            3. 限制返回的记录数量
            4. 转换为对局摘要对象列表
        
        使用场景:
            - 对局历史页面
            - 用户战绩查看
        """
        # 从数据库查询对局记录
        # filter: 添加查询条件（用户ID等于指定值）
        # order_by: 按创建时间倒序排列（desc()表示降序）
        # limit(): 限制返回的记录数量
        # all(): 获取所有匹配的记录
        matches = db.query(Match).filter(
            Match.user_id == user_id
        ).order_by(Match.created_at.desc()).limit(limit).all()
        
        # 将数据库记录转换为对局摘要对象列表
        # 使用列表推导式，简洁高效
        return [
            MatchSummary(
                id=match.id,
                hero_name=match.hero_name,
                position=match.position,
                result=match.result,
                duration=match.duration,
                kda=match.kda,
                participation_rate=match.participation_rate,
                created_at=match.created_at
            )
            for match in matches
        ]
    
    def get_summary(self, match_id: str, db: Session) -> MatchSummary:
        """
        获取对局摘要
        
        参数:
            match_id: 对局ID
            db: 数据库会话对象
        
        返回:
            MatchSummary: 对局摘要对象，如果对局不存在则返回None
        
        功能:
            - 查询对局的摘要信息
            - 返回对局的基本数据
        
        业务逻辑:
            1. 根据match_id查询对局
            2. 如果对局不存在，返回None
            3. 如果对局存在，返回对局摘要对象
        
        使用场景:
            - 对局详情页面
            - 对局数据分析
        """
        # 从数据库查询对局
        # filter: 添加查询条件（对局ID等于指定值）
        # first(): 获取第一条记录，如果没有则返回None
        match = db.query(Match).filter(Match.id == match_id).first()
        
        # 如果对局不存在，返回None
        if not match:
            return None
        
        # 对局存在，返回对局摘要对象
        return MatchSummary(
            id=match.id,
            hero_name=match.hero_name,
            position=match.position,
            result=match.result,
            duration=match.duration,
            kda=match.kda,
            participation_rate=match.participation_rate,
            created_at=match.created_at
        )
    
    def delete_match(self, match_id: str, db: Session):
        """
        删除对局记录
        
        参数:
            match_id: 对局ID
            db: 数据库会话对象
        
        返回:
            None
        
        功能:
            - 删除指定的对局记录
            - 用于用户清理对局历史
        
        业务逻辑:
            1. 根据match_id删除对局记录
            2. 提交事务
        
        注意:
            - 此操作不可逆，请谨慎使用
            - 删除后无法恢复
        
        使用场景:
            - 用户删除对局记录
            - 数据清理
        """
        # 删除指定的对局记录
        # filter: 添加查询条件（对局ID等于指定值）
        # delete(): 删除所有匹配的记录
        db.query(Match).filter(Match.id == match_id).delete()
        
        # 提交事务，保存删除操作
        db.commit()
