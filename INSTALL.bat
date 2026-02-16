@echo off
chcp 65001 >nul
echo ====================================
echo 王者荣耀智能助手 - 安装脚本
echo ====================================
echo.

cd /d "%~dp0"

echo [1/4] 创建数据库...
echo 请确保MySQL已安装并运行
echo.
echo 手动执行以下步骤：
echo 1. 打开MySQL命令行客户端
echo 2. 执行: source database/schema.sql;
echo 3. 初始化示例数据: cd database && python init_data.py
echo.
pause

echo [2/4] 安装后端依赖...
cd backend
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
cd ..

echo [3/4] 安装前端依赖...
cd frontend
npm install
cd ..

echo [4/4] 配置环境变量...
echo 请编辑 backend/.env 文件，配置以下内容：
echo - DATABASE_URL: MySQL数据库连接字符串
echo - ZHIPUAI_API_KEY: 智谱AI API密钥
echo - SECRET_KEY: 密钥
echo.

echo ====================================
echo 安装完成！
echo 请完成上述配置后运行 START.bat 启动服务
echo ====================================
pause
