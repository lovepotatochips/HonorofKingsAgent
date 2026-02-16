# 导入FastAPI的APIRouter类，用于创建API路由
# APIRouter是FastAPI的路由组件，用于组织API端点
from fastapi import APIRouter

# 导入所有API端点模块
# chat: 聊天相关的API端点
# hero: 英雄相关的API端点
# user: 用户相关的API端点
# match: 对局相关的API端点
# analysis: 分析相关的API端点
from app.api.v1.endpoints import chat, hero, user, match, analysis

# ==================== v1版本API路由器初始化 ====================

# 创建v1版本的API路由器
# 这个路由器将包含所有v1版本的API端点
api_router = APIRouter()

# ==================== 路由注册 ====================

# 注册聊天相关的API端点
# chat.router: 聊天模块的路由器
# prefix="/chat": 所有聊天API的路径前缀为 /chat
# tags=["chat"]: 在API文档中分组显示，标签为"chat"
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])

# 注册英雄相关的API端点
# hero.router: 英雄模块的路由器
# prefix="/hero": 所有英雄API的路径前缀为 /hero
# tags=["hero"]: 在API文档中分组显示，标签为"hero"
api_router.include_router(hero.router, prefix="/hero", tags=["hero"])

# 注册用户相关的API端点
# user.router: 用户模块的路由器
# prefix="/user": 所有用户API的路径前缀为 /user
# tags=["user"]: 在API文档中分组显示，标签为"user"
api_router.include_router(user.router, prefix="/user", tags=["user"])

# 注册对局相关的API端点
# match.router: 对局模块的路由器
# prefix="/match": 所有对局API的路径前缀为 /match
# tags=["match"]: 在API文档中分组显示，标签为"match"
api_router.include_router(match.router, prefix="/match", tags=["match"])

# 注册分析相关的API端点
# analysis.router: 分析模块的路由器
# prefix="/analysis": 所有分析API的路径前缀为 /analysis
# tags=["analysis"]: 在API文档中分组显示，标签为"analysis"
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
