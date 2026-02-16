# 开发指南

## 项目结构

```
HonorofKingsAgent/
├── backend/              # 后端服务
│   ├── app/
│   │   ├── api/         # API路由
│   │   ├── core/        # 核心配置
│   │   ├── models/      # 数据模型
│   │   ├── services/    # 业务逻辑
│   │   └── schemas/     # 请求/响应模型
│   ├── tests/           # 测试文件
│   └── requirements.txt # 依赖列表
├── frontend/            # 前端应用
│   ├── src/
│   │   ├── api/        # API调用
│   │   ├── components/ # 组件
│   │   ├── views/      # 页面
│   │   ├── stores/     # 状态管理
│   │   └── router/     # 路由配置
│   └── package.json
├── database/            # 数据库脚本
│   ├── schema.sql      # 数据库结构
│   └── init_data.py    # 初始数据
└── docs/               # 文档
```

## 后端开发

### 环境要求

- Python 3.13+
- MySQL 8.0+
- Redis (可选)

### 本地开发

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### 添加新API

1. 在 `app/api/v1/endpoints/` 创建新的路由文件
2. 在 `app/schemas/` 定义请求/响应模型
3. 在 `app/services/` 实现业务逻辑
4. 在 `app/api/v1/__init__.py` 注册路由

### 数据库迁移

```bash
cd backend
python database/init_data.py
```

## 前端开发

### 环境要求

- Node.js 18+
- npm 或 yarn

### 本地开发

```bash
cd frontend
npm install
npm run dev
```

### 添加新页面

1. 在 `src/views/` 创建新的页面组件
2. 在 `src/router/index.js` 配置路由
3. 如需API调用，在 `src/api/` 创建对应的API文件

### 状态管理

使用 Pinia 进行状态管理，Store文件位于 `src/stores/`。

## 测试

### 后端测试

```bash
cd backend
pytest
```

### 前端测试

```bash
cd frontend
npm run test
```

## 部署

### 后端部署

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 前端部署

```bash
cd frontend
npm run build
```

生成的静态文件位于 `dist/` 目录，可部署到任何静态文件服务器。

## 代码规范

- 后端遵循 PEP 8 规范
- 前端遵循 ESLint 规范
- 提交前运行 lint 检查

## 注意事项

1. 所有API请求都经过统一的错误处理
2. 使用环境变量管理配置
3. 数据库操作使用 ORM (SQLAlchemy)
4. 前端响应式设计，适配移动端
