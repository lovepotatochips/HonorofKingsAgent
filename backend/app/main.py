# 导入FastAPI框架的核心类，用于创建Web应用
from fastapi import FastAPI

# 导入CORS中间件，用于处理跨域请求
# 跨域资源共享（CORS）允许前端从不同域名访问后端API
from fastapi.middleware.cors import CORSMiddleware

# 导入静态文件处理模块，用于提供静态资源（如图片、CSS、JS等）
from fastapi.staticfiles import StaticFiles

# 导入异步上下文管理器，用于管理应用的生命周期（启动和关闭）
from contextlib import asynccontextmanager

# 导入Uvicorn服务器，用于运行FastAPI应用
import uvicorn

# 导入应用配置模块，包含项目的各种配置信息
from app.core.config import settings

# 导入数据库初始化和关闭函数
from app.core.database import init_db, close_db

# 导入API路由模块，包含所有API端点
from app.api import api_router


# 定义应用生命周期管理函数
# 这是一个异步上下文管理器，用于在应用启动和关闭时执行特定操作
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理器
    
    参数:
        app: FastAPI应用实例
    
    功能:
        1. 应用启动时执行 startup() 函数
        2. 应用运行期间 yield 保持连接
        3. 应用关闭时执行 shutdown() 函数
    """
    # 应用启动时执行初始化操作
    startup()
    # yield 让应用正常运行
    yield
    # 应用关闭时执行清理操作
    shutdown()


def startup():
    """
    应用启动时执行的初始化函数
    
    功能:
        - 初始化数据库连接
        - 创建数据库表（如果不存在）
        - 执行其他启动时的必要操作
    """
    # 调用数据库初始化函数
    init_db()


def shutdown():
    """
    应用关闭时执行的清理函数
    
    功能:
        - 关闭数据库连接
        - 执行其他关闭时的清理操作
    """
    # 调用数据库关闭函数
    close_db()


# 创建FastAPI应用实例
# FastAPI是现代、快速的Web框架，用于构建API
app = FastAPI(
    # 设置API标题，在文档页面显示
    title=settings.PROJECT_NAME,
    # 设置API描述信息
    description="王者荣耀智能助手API",
    # 设置API版本号
    version=settings.VERSION,
    # 设置OpenAPI文档的URL路径
    # OpenAPI是API文档规范，FastAPI自动生成API文档
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    # 设置生命周期管理器
    lifespan=lifespan
)

# 添加CORS中间件
# CORS（跨域资源共享）允许浏览器从不同域访问API
# 这对于前后端分离的项目是必需的
app.add_middleware(
    # 指定中间件类型为CORS
    CORSMiddleware,
    # 允许的源（域名）列表
    # * 表示允许所有域名，生产环境应该指定具体的域名
    allow_origins=settings.CORS_ORIGINS,
    # 允许携带凭证（如cookies）
    allow_credentials=True,
    # 允许的HTTP方法（GET、POST、PUT、DELETE等）
    # * 表示允许所有方法
    allow_methods=["*"],
    # 允许的HTTP头（如Content-Type、Authorization等）
    # * 表示允许所有头
    allow_headers=["*"],
)

# 包含API路由
# 将所有API端点注册到应用中，并设置统一的前缀
app.include_router(
    api_router,  # 路由模块
    prefix=settings.API_V1_STR  # API前缀，如 /api/v1
)


# 定义根路径的API端点
# 访问 http://localhost:8000/ 时会调用此函数
@app.get("/")
async def root():
    """
    根路径API端点
    
    返回:
        包含API基本信息和状态的字典
    
    功能:
        - 提供API的基本信息
        - 用于测试API是否正常运行
    """
    return {
        # API的消息描述
        "message": "王者荣耀智能助手API",
        # API的版本号
        "version": settings.VERSION,
        # API的运行状态
        "status": "running"
    }


# 定义健康检查API端点
# 访问 http://localhost:8000/health 时会调用此函数
# 常用于负载均衡器或监控系统检查服务是否健康
@app.get("/health")
async def health_check():
    """
    健康检查API端点
    
    返回:
        包含健康状态的字典
    
    功能:
        - 用于监控和负载均衡
        - 检查服务是否正常运行
    """
    return {
        # 返回健康状态
        "status": "healthy"
    }


# 主程序入口
# 当直接运行此文件时执行以下代码
if __name__ == "__main__":
    # 使用Uvicorn服务器运行FastAPI应用
    uvicorn.run(
        # 应用的位置，格式为 "模块:应用实例"
        "app.main:app",
        # 监听所有网络接口（0.0.0.0），允许外部访问
        # 如果设置为127.0.0.1，则只能本地访问
        host="0.0.0.0",
        # 监听的端口号
        port=8000,
        # 是否启用热重载（开发模式下启用，代码修改后自动重启）
        reload=settings.DEBUG
    )
