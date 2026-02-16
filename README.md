# 王者荣耀智能助手

一款合规、轻量化、AI驱动的王者荣耀智能助手应用，支持自然语言交互、智能对局分析和个性化推荐。

## 项目简介

本项目旨在为王者荣耀玩家提供全方位的智能辅助服务，通过AI技术提升游戏体验和竞技水平。应用采用移动端优先设计，支持多设备访问。

### 核心特性

- **AI驱动**：集成GLM-4大语言模型，提供智能对话和分析
- **合规设计**：严格遵守游戏规则，不提供任何外挂或作弊功能
- **轻量化**：采用现代化技术栈，保持应用简洁高效
- **移动优先**：响应式设计，完美适配移动设备
- **智能分析**：自动分析对局数据，提供专业复盘报告

---

## 技术栈

### 后端技术

| 技术 | 版本 | 说明 |
|------|------|------|
| Python | 3.13+ | 后端语言 |
| FastAPI | Latest | Web框架 |
| SQLAlchemy | Latest | ORM框架 |
| SQLite | Latest | 数据库（开发） |
| MySQL/PostgreSQL | 8.0+/14+ | 数据库（生产） |
| Pydantic | Latest | 数据验证 |
| Uvicorn | Latest | ASGI服务器 |

### 前端技术

| 技术 | 版本 | 说明 |
|------|------|------|
| Vue.js | 3.x | 前端框架 |
| Element Plus | Latest | PC端UI组件库 |
| Vant | Latest | 移动端UI组件库 |
| Pinia | Latest | 状态管理 |
| Vue Router | 4.x | 路由管理 |
| Axios | Latest | HTTP客户端 |
| Vite | 5.x | 构建工具 |

### AI服务

| 服务 | 说明 |
|------|------|
| GLM-4 | 智谱AI大语言模型 |

---

## 项目结构

```
HonorofKingsAgent/
├── backend/              # 后端服务
│   ├── app/
│   │   ├── api/         # API路由
│   │   │   └── v1/
│   │   │       └── endpoints/
│   │   │           ├── chat.py      # 对话接口
│   │   │           ├── hero.py      # 英雄接口
│   │   │           ├── match.py     # 对局接口
│   │   │           ├── user.py      # 用户接口
│   │   │           └── analysis.py  # 分析接口
│   │   ├── core/        # 核心配置
│   │   │   ├── config.py            # 配置文件
│   │   │   └── database.py          # 数据库配置
│   │   ├── models/      # 数据模型
│   │   │   ├── user.py              # 用户模型
│   │   │   ├── hero.py              # 英雄模型
│   │   │   ├── match.py             # 对局模型
│   │   │   └── conversation.py       # 对话模型
│   │   ├── schemas/     # 数据验证
│   │   ├── services/    # 业务逻辑
│   │   │   ├── chat_service.py      # 对话服务
│   │   │   ├── hero_service.py      # 英雄服务
│   │   │   ├── match_service.py     # 对局服务
│   │   │   ├── analysis_service.py  # 分析服务
│   │   │   ├── ai_service.py        # AI服务
│   │   │   └── intent_service.py    # 意图识别服务
│   │   └── main.py      # 应用入口
│   ├── scripts/         # 工具脚本
│   ├── venv/            # 虚拟环境
│   ├── requirements.txt # Python依赖
│   └── .env            # 环境变量
├── frontend/            # 前端应用
│   ├── src/
│   │   ├── api/        # API调用
│   │   │   ├── chat.js
│   │   │   ├── hero.js
│   │   │   ├── match.js
│   │   │   └── user.js
│   │   ├── assets/     # 静态资源
│   │   │   ├── images/
│   │   │   └── styles/
│   │   ├── components/ # 组件
│   │   │   ├── ChatInput.vue
│   │   │   ├── HeroCard.vue
│   │   │   └── MatchCard.vue
│   │   ├── router/     # 路由配置
│   │   │   └── index.js
│   │   ├── stores/     # 状态管理
│   │   │   ├── chat.js
│   │   │   ├── hero.js
│   │   │   └── user.js
│   │   ├── utils/      # 工具函数
│   │   ├── views/      # 页面
│   │   │   ├── Home.vue         # 首页/对话
│   │   │   ├── Hero.vue         # 英雄列表
│   │   │   ├── HeroDetail.vue   # 英雄详情
│   │   │   ├── Match.vue        # 对局列表
│   │   │   ├── MatchDetail.vue  # 对局详情
│   │   │   └── Profile.vue      # 个人中心
│   │   ├── App.vue
│   │   └── main.js
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── .env.development
├── docs/                # 文档
│   ├── README.md
│   ├── 01-需求说明书.md
│   ├── 02-功能清单.md
│   ├── 03-建设方案.md
│   ├── 04-数据库说明书.md
│   ├── 05-前端页面说明书.md
│   ├── 06-后端接口说明书.md
│   ├── 07-操作手册.md
│   └── 08-部署指南.md
├── .gitignore
├── INSTALL.bat
├── START.bat
└── README.md
```

---

## 核心功能

### 1. AI对话中心

- 自然语言对话交互
- 意图识别与路由
- 多轮对话上下文管理
- 对话历史记录

### 2. 赛前智能规划

- 英雄推荐：根据位置、段位推荐英雄
- 英雄详情：完整的英雄信息和技能介绍
- 装备推荐：基于英雄定位推荐装备
- 铭文推荐：推荐最优铭文搭配
- 克制关系：查看英雄间的克制关系

### 3. 赛中智能辅助

- 英雄技能快速查询
- 装备效果查询
- 实时信息查询

### 4. 赛后AI复盘

- 对局数据展示：KDA、参团率、伤害输出等
- AI智能分析：亮点表现、失误点、改进建议
- 详细报告生成：结构化的复盘报告
- 历史对局记录：对局历史查询和管理
- 数据趋势分析：多局数据对比

### 5. 娱乐互动

- 英雄趣味知识问答
- 游戏梗和段位图鉴
- 热门话题讨论

### 6. 个人中心

- 个人信息展示：昵称、头像、段位、星数
- 游戏数据统计：总场次、胜率、常用英雄
- 偏好设置：界面主题、通知设置、隐私设置
- 数据管理：清除数据、导出数据

---

## 快速开始

### 环境要求

- Python 3.13+
- Node.js 18+
- Git

### Windows快速启动

1. 克隆项目：

```bash
git clone https://github.com/yourusername/HonorofKingsAgent.git
cd HonorofKingsAgent
```

2. 运行安装脚本：

```bash
INSTALL.bat
```

3. 启动应用：

```bash
START.bat
```

### 手动安装

#### 后端安装

1. 创建虚拟环境：

```bash
cd backend
python -m venv venv
```

2. 激活虚拟环境：

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

3. 安装依赖：

```bash
pip install -r requirements.txt
```

4. 配置环境变量：

复制`.env.example`为`.env`，并配置相关参数：

```env
DATABASE_URL=sqlite:///honor_of_kings.db
GLM_API_KEY=your_api_key_here
GLM_API_URL=https://open.bigmodel.cn/api/paas/v4/chat/completions
```

5. 初始化数据库并导入数据：

```bash
python scripts/import_real_hero_data.py
python scripts/import_sample_matches.py
```

6. 启动后端服务：

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问：http://localhost:8000

#### 前端安装

1. 安装依赖：

```bash
cd frontend
npm install
```

2. 配置环境变量：

编辑`.env.development`：

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_TITLE=王者荣耀智能助手
VITE_APP_VERSION=1.0.0
```

3. 启动开发服务器：

```bash
npm run dev
```

访问：http://localhost:5173 或 http://localhost:5174

---

## 访问应用

- **前端地址**：http://localhost:5173 或 http://localhost:5174
- **后端地址**：http://localhost:8000
- **API文档**：http://localhost:8000/docs

---

## 功能使用

### AI对话

1. 访问首页
2. 在输入框中输入问题
3. 点击发送按钮
4. 等待AI回复

### 英雄查询

1. 点击底部导航栏的"英雄"
2. 搜索或筛选英雄
3. 点击英雄查看详情

### 对局分析

1. 点击底部导航栏的"对局"
2. 添加对局数据
3. 查看对局详情和AI分析报告

### 个人中心

1. 点击底部导航栏的"我的"
2. 查看个人信息和统计数据
3. 修改个人设置

---

## 文档

项目提供完整的文档，位于`docs`目录：

- [README](docs/README.md) - 文档导航
- [需求说明书](docs/01-需求说明书.md) - 项目需求与功能规格
- [功能清单](docs/02-功能清单.md) - 完整的功能列表
- [建设方案](docs/03-建设方案.md) - 项目建设方案与技术架构
- [数据库说明书](docs/04-数据库说明书.md) - 数据库设计与表结构
- [前端页面说明书](docs/05-前端页面说明书.md) - 前端页面与组件说明
- [后端接口说明书](docs/06-后端接口说明书.md) - API接口文档
- [操作手册](docs/07-操作手册.md) - 用户操作指南
- [部署指南](docs/08-部署指南.md) - 系统部署与安装

---

## 开发指南

### 代码规范

- 遵循PEP 8（Python）
- 遵循ESLint（JavaScript）
- 统一的命名规范
- 完善的代码注释

### Git规范

- 分支管理：Git Flow
- 提交信息：Conventional Commits
- 代码评审：必需

### 测试

```bash
# 后端测试
cd backend
pytest

# 前端测试
cd frontend
npm run test
```

---

## 合规声明

本项目严格遵守游戏规则和相关法律法规，仅提供：

- 辅助咨询和提醒功能
- 本地数据查询
- AI对话分析
- 合规范围内的游戏建议

不包含：
- 外挂程序
- 内存注入
- 数据修改
- 实时对局数据获取
- 任何违规功能

---

## 许可证

本项目仅供学习和个人使用，请勿用于商业用途。

---

## 贡献

欢迎提交Issue和Pull Request！


---

## 更新日志

### v1.0.0 (2026-02-14)

- 实现AI对话功能
- 实现英雄查询功能
- 实现对局管理和分析功能
- 实现个人中心功能
- 完善文档

---

## 致谢

感谢所有为本项目做出贡献的开发者！

---

**祝您游戏愉快，早日上王者！** 🎮
