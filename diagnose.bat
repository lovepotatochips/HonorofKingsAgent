@echo off
chcp 65001 >nul
echo ======================================================
echo    王者荣耀智能助手 - 诊断工具
echo ======================================================
echo.

echo [诊断1] 检查Git是否安装...
git --version
if %errorlevel% neq 0 (
    echo ❌ Git未安装或不在PATH中
    echo 请先安装Git：https://git-scm.com/download/win
    pause
    exit /b 1
)
echo ✅ Git已安装
echo.

echo [诊断2] 检查Git配置...
git config --global user.name
git config --global user.email
echo.

echo [诊断3] 检查当前分支...
git branch
echo.

echo [诊断4] 检查远程仓库...
git remote -v
echo.

echo [诊断5] 检查提交历史...
git log --oneline -3
echo.

echo [诊断6] 测试GitHub连接...
ping github.com -n 2
echo.

echo ======================================================
echo    诊断完成
echo ======================================================
echo.
echo 如果以上检查都正常，请尝试运行：
echo   push_with_log.bat  （带日志的推送工具）
echo.
echo 如果推送仍然失败，请查看日志文件：git_push.log
echo.
pause
