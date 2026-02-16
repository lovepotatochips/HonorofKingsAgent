# 导入类型提示
# List: 列表类型
from typing import List

# 导入Session类
# Session: SQLAlchemy的数据库会话，用于与数据库交互
from sqlalchemy.orm import Session

# 导入对局和分析模型
# Match: 对局数据库模型
# Analysis: 对局分析数据库模型
from app.models.match import Match, Analysis

# 导入英雄模型
# Hero: 英雄数据库模型
from app.models.hero import Hero

# 导入分析相关的Schema
# AnalysisRequest: 分析请求模型
# AnalysisResponse: 分析响应模型
# AnalysisReport: 分析报告模型
from app.schemas.analysis import AnalysisRequest, AnalysisResponse, AnalysisReport

# 导入uuid模块
# uuid: 用于生成唯一标识符
import uuid


class AnalysisService:
    """
    对局分析服务类
    
    负责处理对局分析相关的业务逻辑
    
    主要功能:
        - 分析对局表现
        - 生成分析报告
        - 提供改进建议
        - 查询分析报告
    
    设计模式:
        - 服务层模式（Service Layer）
        - 将业务逻辑与数据访问分离
        - 提供清晰的API供控制器调用
    
    使用场景:
        - 对局复盘
        - 表现分析
        - 改进建议
        - 学习提升
    """
    
    async def analyze(self, request: AnalysisRequest, db: Session) -> AnalysisResponse:
        """
        分析对局
        
        参数:
            request: 分析请求，包含对局ID等信息
            db: 数据库会话对象
        
        返回:
            AnalysisResponse: 分析响应，包含分析结果
        
        功能:
            - 分析对局表现
            - 生成亮点、失误和建议
            - 生成分析报告
            - 保存分析结果
        
        业务逻辑:
            1. 查询对局记录
            2. 分析对局表现（KDA、参团率等）
            3. 生成亮点、失误和建议
            4. 生成分析报告
            5. 保存分析结果到数据库
            6. 返回分析响应
        
        异步处理:
            - async: 异步方法，不阻塞主线程
        
        分析指标:
            - KDA: 击杀死亡助攻比
            - 参团率: 团战参与度
            - 输出伤害: 伤害贡献
            - 死亡次数: 生存能力
        """
        # 从数据库查询对局记录
        match = db.query(Match).filter(Match.id == request.match_id).first()
        
        # 如果对局不存在，抛出异常
        if not match:
            raise ValueError("对局记录不存在")
        
        # 分析对局表现
        # 返回整体评价、亮点、失误和建议
        overall_rating, highlights, mistakes, suggestions = self._analyze_match(match, db)
        
        # 生成分析报告
        report = self._generate_report(match, highlights, mistakes, suggestions)
        
        # 创建分析记录对象
        analysis = Analysis(
            # 分析ID
            id=str(uuid.uuid4()),
            # 对局ID
            match_id=request.match_id,
            # 整体评价
            overall_rating=overall_rating,
            # 亮点列表
            highlights=highlights,
            # 失误列表
            mistakes=mistakes,
            # 建议列表
            suggestions=suggestions,
            # 分析报告
            report=report,
            # 改进建议
            improvements=suggestions
        )
        
        # 将分析记录添加到数据库会话
        db.add(analysis)
        # 提交事务，保存分析记录
        db.commit()
        
        # 返回分析响应对象
        return AnalysisResponse(
            analysis_id=analysis.id,
            overall_rating=overall_rating,
            # 提取亮点文本
            highlights=[h.get("text", "") for h in highlights],
            # 提取失误文本
            mistakes=[m.get("text", "") for m in mistakes],
            # 提取建议文本
            suggestions=[s.get("text", "") for s in suggestions],
            report=report
        )
    
    def get_report(self, analysis_id: str, db: Session) -> dict:
        """
        获取分析报告
        
        参数:
            analysis_id: 分析ID
            db: 数据库会话对象
        
        返回:
            dict: 分析报告数据，如果分析不存在则返回None
        
        功能:
            - 查询分析报告
            - 返回详细的分析结果
        
        业务逻辑:
            1. 根据analysis_id查询分析记录
            2. 如果分析不存在，返回None
            3. 如果分析存在，返回分析报告数据
        
        注意:
            - 将datetime对象转换为ISO格式字符串
            - 避免序列化错误
        
        使用场景:
            - 查看分析报告
            - 对局复盘详情
        """
        # 从数据库查询分析记录
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        
        # 如果分析不存在，返回None
        if not analysis:
            return None
        
        # 返回分析报告数据
        return {
            # 分析ID
            "id": analysis.id,
            # 对局ID
            "match_id": analysis.match_id,
            # 整体评价
            "overall_rating": analysis.overall_rating,
            # 亮点列表
            "highlights": analysis.highlights or [],
            # 失误列表
            "mistakes": analysis.mistakes or [],
            # 建议列表
            "suggestions": analysis.suggestions or [],
            # 分析报告
            "report": analysis.report,
            # 改进建议
            "improvements": analysis.improvements or [],
            # 创建时间（转换为ISO格式字符串）
            "created_at": analysis.created_at.isoformat() if analysis.created_at else None
        }
    
    def get_suggestions(self, hero_id: int, db: Session) -> dict:
        """
        获取英雄建议
        
        参数:
            hero_id: 英雄ID
            db: 数据库会话对象
        
        返回:
            dict: 英雄建议数据
        
        功能:
            - 提供英雄的通用建议
            - 帮助玩家提升英雄熟练度
        
        业务逻辑:
            1. 查询英雄信息
            2. 如果英雄不存在，返回错误
            3. 如果英雄存在，返回英雄建议
        
        建议内容:
            - 通用建议：发育、技能、支援、出装
            - 英雄提示：定位、难度、练习
        
        使用场景:
            - 英雄学习
            - 技能提升
            - 策略学习
        """
        # 从数据库查询英雄
        hero = db.query(Hero).filter(Hero.id == hero_id).first()
        
        # 如果英雄不存在，返回错误
        if not hero:
            return {"error": "英雄不存在"}
        
        # 返回英雄建议数据
        return {
            # 英雄ID
            "hero_id": hero_id,
            # 英雄名称
            "hero_name": hero.name,
            # 通用建议列表
            "suggestions": [
                "关注经济发育，避免过早参团",
                "合理使用技能，注意技能冷却时间",
                "观察小地图，及时支援队友",
                "根据局势调整出装思路"
            ],
            # 英雄提示列表
            "tips": [
                f"{hero.name}的定位是{hero.position}",
                f"难度等级：{hero.difficulty}",
                "多练习技能连招，提高熟练度"
            ]
        }
    
    def _analyze_match(self, match: Match, db: Session) -> tuple:
        """
        分析对局表现
        
        参数:
            match: 对局记录
            db: 数据库会话对象
        
        返回:
            tuple: (整体评价, 亮点列表, 失误列表, 建议列表)
        
        功能:
            - 分析对局的关键指标
            - 生成亮点、失误和建议
            - 评估整体表现
        
        业务逻辑:
            1. 初始化亮点、失误和建议列表
            2. 分析KDA表现
            3. 分析参团率表现
            4. 分析死亡次数
            5. 分析输出伤害
            6. 生成整体评价
            7. 返回分析结果
        
        分析标准:
            - KDA >= 5: 优秀
            - KDA >= 3: 良好
            - KDA < 3: 需要改进
            - 参团率 >= 70%: 优秀
            - 参团率 >= 50%: 一般
            - 参团率 < 50%: 需要改进
        
        私有方法:
            - 以下划线开头，表示内部方法
            - 只在类内部使用，不对外暴露
        """
        # 初始化亮点、失误和建议列表
        highlights = []
        mistakes = []
        suggestions = []
        
        # 获取KDA和参团率
        kda = match.kda or 0
        participation = match.participation_rate or 0
        
        # ==================== 分析KDA表现 ====================
        
        # KDA >= 5: 优秀
        if kda >= 5:
            highlights.append({"text": f"KDA表现优秀({kda:.1f})，发育和击杀平衡"})
        # KDA >= 3: 良好
        elif kda >= 3:
            highlights.append({"text": f"KDA表现良好({kda:.1f})，整体发挥稳定"})
        # KDA < 3: 需要改进
        else:
            mistakes.append({"text": f"KDA较低({kda:.1f})，需要提高生存能力"})
        
        # ==================== 分析参团率表现 ====================
        
        # 参团率 >= 70%: 优秀
        if participation >= 70:
            highlights.append({"text": f"参团率高({participation:.1f}%)，团战参与积极"})
        # 参团率 >= 50%: 一般
        elif participation >= 50:
            suggestions.append({"text": f"参团率一般({participation:.1f}%)，建议多参与团战"})
        # 参团率 < 50%: 需要改进
        else:
            mistakes.append({"text": f"参团率低({participation:.1f}%)，团队贡献不足"})
            suggestions.append({"text": "提高团战参与度，及时支援队友"})
        
        # ==================== 分析死亡次数 ====================
        
        # 如果死亡次数超过8次，添加失误和建议
        if match.deaths and match.deaths > 8:
            mistakes.append({"text": f"死亡次数过多({match.deaths}次)，需要注意走位"})
            suggestions.append({"text": "提高走位意识，避免被gank"})
        
        # ==================== 分析输出伤害 ====================
        
        # 如果输出伤害超过10万，添加亮点
        if match.damage and match.damage > 100000:
            highlights.append({"text": f"输出伤害高({match.damage})，发育良好"})
        
        # ==================== 生成改进建议 ====================
        
        # 如果有失误，添加改进建议
        if mistakes:
            suggestions.append({"text": "复盘时重点关注失误点，避免重复犯错"})
        
        # ==================== 评估整体表现 ====================
        
        # 根据KDA和参团率评估整体表现
        overall_rating = "优秀" if kda >= 4 and participation >= 60 else \
                         "良好" if kda >= 2.5 and participation >= 40 else \
                         "一般" if kda >= 1.5 and participation >= 30 else "需要改进"
        
        # 返回分析结果
        return overall_rating, highlights, mistakes, suggestions
    
    def _generate_report(self, match: Match, highlights: List, mistakes: List, suggestions: List) -> str:
        """
        生成分析报告
        
        参数:
            match: 对局记录
            highlights: 亮点列表
            mistakes: 失误列表
            suggestions: 建议列表
        
        返回:
            str: 分析报告文本
        
        功能:
            - 生成详细的分析报告
            - 包含对局数据、亮点、失误和建议
        
        业务逻辑:
            1. 构建报告标题和对局信息
            2. 添加亮点部分
            3. 添加失误部分
            4. 添加建议部分
            5. 返回报告文本
        
        报告格式:
            - 标题
            - 对局基本信息
            - 亮点表现
            - 需要改进
            - 改进建议
        
        私有方法:
            - 以下划线开头，表示内部方法
            - 只在类内部使用，不对外暴露
        """
        # 初始化报告行列表
        report_lines = [
            # 报告标题
            f"对局复盘报告",
            # 对局基本信息
            f"英雄：{match.hero_name} | 位置：{match.position}",
            # KDA和参团率
            f"KDA：{match.kda:.1f} | 参团率：{match.participation_rate:.1f}%",
            # 击杀/死亡/助攻
            f"击杀/死亡/助攻：{match.kills}/{match.deaths}/{match.assists}",
            # 空行
            "",
            # 亮点表现标题
            "亮点表现："
        ]
        
        # 如果有亮点，添加亮点列表
        if highlights:
            for highlight in highlights:
                report_lines.append(f"• {highlight.get('text', '')}")
        # 如果没有亮点，添加默认文本
        else:
            report_lines.append("• 暂无明显亮点")
        
        # 添加空行和失误标题
        report_lines.extend([
            "",
            "需要改进："
        ])
        
        # 如果有失误，添加失误列表
        if mistakes:
            for mistake in mistakes:
                report_lines.append(f"• {mistake.get('text', '')}")
        # 如果没有失误，添加默认文本
        else:
            report_lines.append("• 整体表现良好")
        
        # 添加空行和建议标题
        report_lines.extend([
            "",
            "改进建议："
        ])
        
        # 如果有建议，添加建议列表
        if suggestions:
            for suggestion in suggestions:
                report_lines.append(f"• {suggestion.get('text', '')}")
        
        # 将报告行列表合并为字符串，使用换行符分隔
        return "\n".join(report_lines)
