# 导入create_engine函数，用于创建数据库引擎
# 数据库引擎负责连接数据库、执行SQL语句等底层操作
from sqlalchemy import create_engine

# 导入declarative_base，用于创建ORM模型的基类
# ORM（对象关系映射）将Python类映射到数据库表
from sqlalchemy.ext.declarative import declarative_base

# 导入sessionmaker和Session，用于创建数据库会话
# 会话是ORM与数据库交互的接口，负责事务管理
from sqlalchemy.orm import sessionmaker, Session

# 导入配置模块
from app.core.config import settings


# ==================== 数据库引擎配置 ====================

# 创建数据库引擎
# 数据库引擎是SQLAlchemy与数据库交互的核心组件
engine = create_engine(
    # 数据库连接URL，从配置中读取
    # SQLite格式: sqlite:///文件路径
    # MySQL格式: mysql+pymysql://用户:密码@主机:端口/数据库
    settings.DATABASE_URL,
    
    # 启用连接池预检
    # 每次从连接池获取连接时，先发送ping命令测试连接是否有效
    # 避免使用已断开的连接导致错误
    pool_pre_ping=True,
    
    # 连接回收时间（秒）
    # 连接在池中最多存活3600秒（1小时），超过则被回收
    # 避免长时间连接导致的问题
    pool_recycle=3600,
    
    # 是否在控制台打印SQL语句
    # DEBUG=True: 打印SQL，便于调试
    # DEBUG=False: 不打印SQL，提高性能
    echo=settings.DEBUG
)


# ==================== 会话工厂配置 ====================

# 创建会话工厂
# 会话工厂用于创建数据库会话实例
SessionLocal = sessionmaker(
    # 禁用自动提交
    # True: 每次操作自动提交，不利于事务控制
    # False: 需要手动调用commit()提交，推荐使用
    autocommit=False,
    
    # 禁用自动刷新
    # True: 每次查询后自动刷新对象状态
    # False: 需要手动调用refresh()，提高性能
    autoflush=False,
    
    # 绑定到数据库引擎
    bind=engine
)


# ==================== ORM基类配置 ====================

# 创建ORM模型的基类
# 所有数据库模型类都继承自这个Base
Base = declarative_base()


# ==================== 数据库会话管理 ====================

def get_db() -> Session:
    """
    获取数据库会话（依赖注入）
    
    返回:
        Session: 数据库会话对象
    
    功能:
        - 为每个请求创建独立的数据库会话
        - 自动管理会话的生命周期
        - 使用依赖注入，在API端点中自动提供db参数
    
    使用示例:
        @app.get("/heroes")
        def get_heroes(db: Session = Depends(get_db)):
            heroes = db.query(Hero).all()
            return heroes
    
    注意:
        - 使用yield生成器，确保会话在使用后被正确关闭
        - try-finally结构保证即使出错也会关闭会话
    """
    # 创建新的数据库会话
    db = SessionLocal()
    try:
        # yield将db提供给调用者
        yield db
    finally:
        # 无论是否出错，都关闭会话
        db.close()


# ==================== 数据库初始化 ====================

def init_db():
    """
    初始化数据库
    
    功能:
        - 创建所有数据库表（如果不存在）
        - 根据ORM模型定义创建表结构
        - 不会删除已存在的表或数据
    
    使用场景:
        - 应用首次启动时
        - 数据库迁移后
    
    注意:
        - 不会修改已存在的表结构
        - 如需修改表结构，应使用Alembic等迁移工具
    """
    # 导入所有模型模块
    # 必须先导入模型，Base才能感知到所有表定义
    from app.models import hero, user, conversation, match
    
    # 创建所有表
    # create_all会检查表是否存在，只创建不存在的表
    Base.metadata.create_all(bind=engine)


# ==================== 数据库关闭 ====================

def close_db():
    """
    关闭数据库连接
    
    功能:
        - 关闭所有数据库连接
        - 释放数据库资源
        - 清空连接池
    
    使用场景:
        - 应用关闭时
        - 需要重新连接数据库时
    
    注意:
        - 关闭后需要重新初始化才能再次使用
    """
    # 释放数据库引擎的所有连接
    # dispose会关闭连接池中的所有连接
    engine.dispose()
