# 导入FastAPI的APIRouter类，用于创建API路由
# APIRouter是FastAPI的路由组件，用于组织API端点
from fastapi import APIRouter

# 导入v1版本的API路由器
# app.api.v1: v1版本的API模块
# api_router: v1版本的路由器实例
from app.api.v1 import api_router as api_v1_router

# ==================== API路由器初始化 ====================

# 创建主API路由器
# 这个路由器将包含所有版本的API路由
# 便于统一管理和版本控制
api_router = APIRouter()

# ==================== 路由注册 ====================

# 将v1版本的API路由包含到主路由器中
# api_v1_router: v1版本的路由器，包含了所有v1版本的API端点
# include_router(): 将子路由器包含到父路由器中
# 这样所有v1版本的API端点都会被注册到主路由器下
api_router.include_router(api_v1_router)
