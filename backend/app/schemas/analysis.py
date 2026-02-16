# 导入Pydantic的BaseModel类
# BaseModel是Pydantic的核心类，用于创建数据验证和序列化模型
from pydantic import BaseModel

# 导入类型提示
from typing import List, Optional, Dict, Any

# 导入datetime类，用于处理日期时间
from datetime import datetime


class AnalysisRequest(BaseModel):
    """
    对局分析请求模型
    
    用于请求对局分析
    
    功能:
        - 验证分析请求的数据
        - 确保必填字段存在
        - 提供数据类型转换
    
    使用场景:
        - 用户请求对局分析
        - API端点的请求体验证
    
    字段说明:
        match_id: 对局ID（必填）
        user_id: 用户ID（必填）
    """
    
    # 对局ID
    # str: 字符串类型
    # 必填字段，没有默认值
    # 用途: 指定要分析的对局
    match_id: str
    
    # 用户ID
    # str: 字符串类型
    # 必填字段，没有默认值
    # 用途: 标识请求分析的用户
    user_id: str


class AnalysisResponse(BaseModel):
    """
    对局分析响应模型
    
    用于返回分析结果
    
    功能:
        - 序列化分析结果数据
        - 提供分析的关键信息
        - 用于API响应
    
    使用场景:
        - 返回分析结果给前端
        - 展示分析摘要
    
    字段说明:
        analysis_id: 分析报告ID
        overall_rating: 整体评分
        highlights: 高光时刻列表
        mistakes: 失误列表
        suggestions: 建议列表
        report: 详细报告
    """
    
    # 分析报告ID
    # str: 字符串类型
    # 必填字段，没有默认值
    # 用途: 分析报告的唯一标识符
    analysis_id: str
    
    # 整体评分
    # str: 字符串类型
    # 必填字段，没有默认值
    # 用途: AI给出的整体评分
    # 示例: "S"、"A"、"B"、"C"、"D"
    overall_rating: str
    
    # 高光时刻列表
    # List[str]: 字符串列表
    # 必填字段，没有默认值
    # 用途: 对局中的精彩表现描述
    # 示例: ["5:30 成功击杀敌方C位", "12:15 五连绝世"]
    highlights: List[str]
    
    # 失误列表
    # List[str]: 字符串列表
    # 必填字段，没有默认值
    # 用途: 对局中的失误描述
    # 示例: ["8:20 单带过深被Gank", "15:00 团战走位失误"]
    mistakes: List[str]
    
    # 建议列表
    # List[str]: 字符串列表
    # 必填字段，没有默认值
    # 用途: 改进建议
    # 示例: ["注意地图信息，避免单带", "把握团战进场时机"]
    suggestions: List[str]
    
    # 详细报告
    # str: 字符串类型
    # 必填字段，没有默认值
    # 用途: AI生成的详细分析报告
    # 示例: "本局表现优秀，KDA达到5.0。高光时刻包括..."
    report: str


class AnalysisReport(BaseModel):
    """
    对局分析报告模型（完整版）
    
    用于返回完整的分析报告
    
    功能:
        - 序列化完整的分析数据
        - 包含详细的分析内容
        - 支持从ORM对象转换
    
    使用场景:
        - 分析详情页
        - 完整报告展示
        - 数据导出
    
    字段说明:
        id: 分析报告ID
        match_id: 对局ID
        overall_rating: 整体评分
        highlights: 高光时刻列表（详细）
        mistakes: 失误列表（详细）
        suggestions: 建议列表（详细）
        report: 详细报告
        improvements: 改进建议
        created_at: 创建时间
    """
    
    # 分析报告ID
    # str: 字符串类型
    # 必填字段，没有默认值
    # 用途: 分析报告的唯一标识符
    id: str
    
    # 对局ID
    # str: 字符串类型
    # 必填字段，没有默认值
    # 用途: 关联的对局ID
    match_id: str
    
    # 整体评分
    # str: 字符串类型
    # 必填字段，没有默认值
    # 用途: AI给出的整体评分
    overall_rating: str
    
    # 高光时刻列表（详细）
    # List[Dict[str, Any]]: 字典列表
    # 必填字段，没有默认值
    # 用途: 对局中的精彩表现详细信息
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
    highlights: List[Dict[str, Any]]
    
    # 失误列表（详细）
    # List[Dict[str, Any]]: 字典列表
    # 必填字段，没有默认值
    # 用途: 对局中的失误详细信息
    # 示例: [
    #   {
    #     "time": "8:20",
    #     "description": "单带过深被Gank",
    #     "severity": "medium",
    #     "suggestion": "注意地图信息，避免单带"
    #   }
    # ]
    mistakes: List[Dict[str, Any]]
    
    # 建议列表（详细）
    # List[Dict[str, Any]]: 字典列表
    # 必填字段，没有默认值
    # 用途: 改进建议详细信息
    # 示例: [
    #   {
    #     "category": "positioning",
    #     "suggestion": "团战时保持安全距离",
    #     "priority": "high"
    #   }
    # ]
    suggestions: List[Dict[str, Any]]
    
    # 详细报告
    # str: 字符串类型
    # 必填字段，没有默认值
    # 用途: AI生成的详细文字报告
    report: str
    
    # 改进建议
    # List[str]: 字符串列表
    # 必填字段，没有默认值
    # 用途: 长期改进建议
    # 示例: ["练习团战站位", "提高地图意识", "加强英雄熟练度"]
    improvements: List[str]
    
    # 创建时间
    # datetime: 日期时间类型
    # 必填字段，没有默认值
    # 用途: 分析报告的创建时间
    created_at: datetime
    
    class Config:
        """
        Pydantic配置类
        """
        # from_attributes: 允许从ORM对象创建Pydantic模型
        # True: 可以将SQLAlchemy模型转换为Pydantic模型
        from_attributes = True
