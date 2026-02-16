# 导入FastAPI相关模块
# APIRouter: 用于创建API路由
# Depends: 用于依赖注入
# HTTPException: 用于处理HTTP异常
from fastapi import APIRouter, Depends, HTTPException

# 导入Session类
# Session: SQLAlchemy的数据库会话，用于与数据库交互
from sqlalchemy.orm import Session

# 导入数据库依赖
# get_db: 获取数据库会话的依赖函数
from app.core.database import get_db

# 导入分析相关的Schema
# AnalysisRequest: 分析请求模型
# AnalysisResponse: 分析响应模型
# AnalysisReport: 分析报告模型
from app.schemas.analysis import AnalysisRequest, AnalysisResponse, AnalysisReport

# 创建API路由器
router = APIRouter()


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_match(
    request: AnalysisRequest,
    db: Session = Depends(get_db)
):
    """
    分析对局
    
    参数:
        request: 分析请求，包含对局ID等信息
        db: 数据库会话对象（通过依赖注入自动获取）
    
    返回:
        AnalysisResponse: 分析响应，包含分析结果
    
    功能:
        - 分析对局表现
        - 生成亮点、失误和建议
        - 生成分析报告
        - 保存分析结果
    
    业务逻辑:
        1. 调用分析服务分析对局
        2. 返回分析响应
        3. 如果发生异常，返回500错误
    
    HTTP方法:
        - POST: 用于发送数据
    
    路径:
        - /api/v1/analysis/analyze
    
    异步处理:
        - async: 异步方法，不阻塞主线程
    """
    try:
        # 导入分析服务
        # 在方法内部导入，避免循环导入
        from app.services.analysis_service import AnalysisService
        
        # 创建分析服务实例
        analysis_service = AnalysisService()
        
        # 调用分析服务分析对局
        # await: 等待异步操作完成
        result = await analysis_service.analyze(request, db)
        return result
    except Exception as e:
        # 如果发生异常，返回500错误
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/report/{analysis_id}")
async def get_analysis_report(
    analysis_id: str,
    db: Session = Depends(get_db)
):
    """
    获取分析报告
    
    参数:
        analysis_id: 分析ID（路径参数）
        db: 数据库会话对象（通过依赖注入自动获取）
    
    返回:
        dict: 分析报告数据
    
    功能:
        - 查询分析报告
        - 返回详细的分析结果
    
    业务逻辑:
        1. 调用分析服务获取分析报告
        2. 如果分析不存在，返回404错误
        3. 如果分析存在，返回分析报告数据
        4. 如果发生异常，返回500错误
    
    HTTP方法:
        - GET: 用于获取数据
    
    路径:
        - /api/v1/analysis/report/{analysis_id}
    
    注意:
        - 将datetime对象转换为ISO格式字符串
        - 避免序列化错误
    """
    try:
        # 导入分析服务
        # 在方法内部导入，避免循环导入
        from app.services.analysis_service import AnalysisService
        
        # 创建分析服务实例
        analysis_service = AnalysisService()
        
        # 调用分析服务获取分析报告
        report = analysis_service.get_report(analysis_id, db)
        
        # 如果分析不存在，返回404错误
        if not report:
            raise HTTPException(status_code=404, detail="分析报告不存在")
        
        return report
    except HTTPException:
        # 如果是HTTP异常，直接抛出
        raise
    except Exception as e:
        # 如果发生其他异常，打印错误堆栈并返回500错误
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/suggestions/{hero_id}")
async def get_improvement_suggestions(
    hero_id: int,
    db: Session = Depends(get_db)
):
    """
    获取改进建议
    
    参数:
        hero_id: 英雄ID（路径参数）
        db: 数据库会话对象（通过依赖注入自动获取）
    
    返回:
        dict: 英雄建议数据
    
    功能:
        - 提供英雄的通用建议
        - 帮助玩家提升英雄熟练度
    
    业务逻辑:
        1. 调用分析服务获取英雄建议
        2. 返回英雄建议数据
        3. 如果发生异常，返回500错误
    
    HTTP方法:
        - GET: 用于获取数据
    
    路径:
        - /api/v1/analysis/suggestions/{hero_id}
    
    建议内容:
        - 通用建议：发育、技能、支援、出装
        - 英雄提示：定位、难度、练习
    """
    try:
        # 导入分析服务
        # 在方法内部导入，避免循环导入
        from app.services.analysis_service import AnalysisService
        
        # 创建分析服务实例
        analysis_service = AnalysisService()
        
        # 调用分析服务获取英雄建议
        suggestions = analysis_service.get_suggestions(hero_id, db)
        return suggestions
    except Exception as e:
        # 如果发生异常，返回500错误
        raise HTTPException(status_code=500, detail=str(e))
