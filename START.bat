@echo off
chcp 65001 >nul
echo ====================================
echo 王者荣耀智能助手 - 快速启动
echo ====================================
echo.

cd /d "%~dp0"

echo [1/3] 检查后端环境...
if not exist "backend\venv" (
    echo 正在创建Python虚拟环境...
    python -m venv backend\venv
)

echo 激活虚拟环境...
call backend\venv\Scripts\activate.bat

echo 安装后端依赖...
pip install -r backend\requirements.txt

echo [2/3] 检查前端环境...
if not exist "frontend\node_modules" (
    echo 正在安装前端依赖...
    cd frontend
    call npm install
    cd ..
)

echo [3/3] 启动服务...
echo.
echo 启动后端服务...
start "后端服务" cmd /k "cd backend && venv\Scripts\activate.bat && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo 等待后端启动...
timeout /t 3 /nobreak >nul

echo 启动前端服务...
start "前端服务" cmd /k "cd frontend && npm run dev"

echo.
echo ====================================
echo 服务启动完成！
echo 后端地址: http://localhost:8000
echo 前端地址: http://localhost:5173
echo API文档: http://localhost:8000/docs
echo ====================================
echo.
echo 按任意键关闭此窗口...
pause >nul
