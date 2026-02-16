# 导入FastAPI相关模块
# APIRouter: 用于创建API路由
# Depends: 用于依赖注入
# HTTPException: 用于处理HTTP异常
# Query: 用于查询参数
from fastapi import APIRouter, Depends, HTTPException, Query

# 导入Session类
# Session: SQLAlchemy的数据库会话，用于与数据库交互
from sqlalchemy.orm import Session

# 导入类型提示
# List: 列表类型
# Optional: 可选类型（可以为None）
from typing import List, Optional

# 导入数据库依赖
# get_db: 获取数据库会话的依赖函数
from app.core.database import get_db

# 导入英雄服务
# HeroService: 英雄服务，负责处理英雄相关逻辑
from app.services.hero_service import HeroService

# 导入英雄相关的Schema
# HeroResponse: 英雄响应模型
# HeroDetailResponse: 英雄详情响应模型
# EquipmentResponse: 装备响应模型
from app.schemas.hero import HeroResponse, HeroDetailResponse, EquipmentResponse

# 创建API路由器
router = APIRouter()

# 创建英雄服务实例
hero_service = HeroService()


@router.get("/list", response_model=List[HeroResponse])
async def get_hero_list(
    position: Optional[str] = None,
    difficulty: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    获取英雄列表
    
    参数:
        position: 英雄位置过滤（查询参数，可选）
        difficulty: 难度过滤（查询参数，可选）
        search: 搜索关键词（查询参数，可选）
        db: 数据库会话对象（通过依赖注入自动获取）
    
    返回:
        List[HeroResponse]: 英雄列表
    
    功能:
        - 查询英雄列表
        - 支持按位置过滤
        - 支持按难度过滤
        - 支持关键词搜索
    
    业务逻辑:
        1. 调用英雄服务获取英雄列表
        2. 返回英雄列表
        3. 如果发生异常，返回500错误
    
    HTTP方法:
        - GET: 用于获取数据
    
    路径:
        - /api/v1/hero/list
    """
    try:
        # 调用英雄服务获取英雄列表
        heroes = hero_service.get_hero_list(position, difficulty, search, db)
        return heroes
    except Exception as e:
        # 如果发生异常，返回500错误
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{hero_id}", response_model=HeroDetailResponse)
async def get_hero_detail(
    hero_id: int,
    db: Session = Depends(get_db)
):
    """
    获取英雄详情
    
    参数:
        hero_id: 英雄ID（路径参数）
        db: 数据库会话对象（通过依赖注入自动获取）
    
    返回:
        HeroDetailResponse: 英雄详情对象
    
    功能:
        - 查询英雄的详细信息
        - 包含技能、克制关系等信息
    
    业务逻辑:
        1. 调用英雄服务获取英雄详情
        2. 如果英雄不存在，返回404错误
        3. 如果英雄存在，返回英雄详情
        4. 如果发生异常，返回500错误
    
    HTTP方法:
        - GET: 用于获取数据
    
    路径:
        - /api/v1/hero/{hero_id}
    """
    try:
        # 调用英雄服务获取英雄详情
        hero = hero_service.get_hero_detail(hero_id, db)
        
        # 如果英雄不存在，返回404错误
        if not hero:
            raise HTTPException(status_code=404, detail="英雄不存在")
        
        return hero
    except HTTPException:
        # 如果是HTTP异常，直接抛出
        raise
    except Exception as e:
        # 如果发生其他异常，返回500错误
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{hero_id}/equipment", response_model=List[EquipmentResponse])
async def get_hero_equipment(
    hero_id: int,
    rank: Optional[str] = "全部",
    db: Session = Depends(get_db)
):
    """
    获取英雄装备推荐
    
    参数:
        hero_id: 英雄ID（路径参数）
        rank: 段位（查询参数，默认"全部"）
        db: 数据库会话对象（通过依赖注入自动获取）
    
    返回:
        List[EquipmentResponse]: 装备推荐列表
    
    功能:
        - 查询英雄的装备推荐
        - 支持按段位过滤
        - 提供不同位置的出装建议
    
    业务逻辑:
        1. 调用英雄服务获取装备推荐
        2. 返回装备推荐列表
        3. 如果发生异常，返回500错误
    
    HTTP方法:
        - GET: 用于获取数据
    
    路径:
        - /api/v1/hero/{hero_id}/equipment
    """
    try:
        # 调用英雄服务获取装备推荐
        equipment = hero_service.get_hero_equipment(hero_id, rank, db)
        return equipment
    except Exception as e:
        # 如果发生异常，返回500错误
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{hero_id}/inscription")
async def get_hero_inscription(
    hero_id: int,
    rank: Optional[str] = "全部",
    db: Session = Depends(get_db)
):
    """
    获取英雄铭文推荐
    
    参数:
        hero_id: 英雄ID（路径参数）
        rank: 段位（查询参数，默认"全部"）
        db: 数据库会话对象（通过依赖注入自动获取）
    
    返回:
        dict: 铭文推荐数据
    
    功能:
        - 查询英雄的铭文推荐
        - 支持按段位过滤
        - 返回铭文配置和描述
    
    业务逻辑:
        1. 调用英雄服务获取铭文推荐
        2. 返回铭文推荐数据
        3. 如果发生异常，返回500错误
    
    HTTP方法:
        - GET: 用于获取数据
    
    路径:
        - /api/v1/hero/{hero_id}/inscription
    """
    try:
        # 调用英雄服务获取铭文推荐
        inscription = hero_service.get_hero_inscription(hero_id, rank, db)
        return inscription
    except Exception as e:
        # 如果发生异常，返回500错误
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bp/suggestion")
async def get_bp_suggestion(
    our_heroes: List[str],
    enemy_heroes: List[str],
    db: Session = Depends(get_db)
):
    """
    获取BP（Ban/Pick）建议
    
    参数:
        our_heroes: 我方英雄列表（请求体）
        enemy_heroes: 敌方英雄列表（请求体）
        db: 数据库会话对象（通过依赖注入自动获取）
    
    返回:
        dict: BP建议数据
    
    功能:
        - 分析阵容短板
        - 生成禁选建议
        - 提供counter英雄推荐
        - 评估整体阵容优势
    
    业务逻辑:
        1. 调用英雄服务获取BP建议
        2. 返回BP建议数据
        3. 如果发生异常，返回500错误
    
    HTTP方法:
        - POST: 用于发送数据
    
    路径:
        - /api/v1/hero/bp/suggestion
    """
    try:
        # 调用英雄服务获取BP建议
        suggestion = hero_service.get_bp_suggestion(our_heroes, enemy_heroes, db)
        return suggestion
    except Exception as e:
        # 如果发生异常，返回500错误
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/categories/positions")
async def get_positions():
    """
    获取英雄位置列表
    
    返回:
        dict: 位置列表
    
    功能:
        - 返回所有英雄位置
        - 用于前端展示位置选择器
    
    位置类型:
        - tank: 坦克
        - warrior: 战士
        - assassin: 刺客
        - mage: 法师
        - archer: 射手
        - support: 辅助
    
    HTTP方法:
        - GET: 用于获取数据
    
    路径:
        - /api/v1/hero/categories/positions
    """
    # 返回位置列表
    return {
        "positions": [
            {"id": "tank", "name": "坦克"},
            {"id": "warrior", "name": "战士"},
            {"id": "assassin", "name": "刺客"},
            {"id": "mage", "name": "法师"},
            {"id": "archer", "name": "射手"},
            {"id": "support", "name": "辅助"}
        ]
    }


@router.get("/categories/difficulties")
async def get_difficulties():
    """
    获取难度列表
    
    返回:
        dict: 难度列表
    
    功能:
        - 返回所有难度等级
        - 用于前端展示难度选择器
    
    难度类型:
        - easy: 简单
        - medium: 中等
        - hard: 困难
    
    HTTP方法:
        - GET: 用于获取数据
    
    路径:
        - /api/v1/hero/categories/difficulties
    """
    # 返回难度列表
    return {
        "difficulties": [
            {"id": "easy", "name": "简单"},
            {"id": "medium", "name": "中等"},
            {"id": "hard", "name": "困难"}
        ]
    }
