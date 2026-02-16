@echo off
chcp 65001 >nul
echo ======================================================
echo    王者荣耀智能助手 - GitHub推送工具
echo ======================================================
echo.
echo [1/3] 正在推送到GitHub...
echo.

cd /d "%~dp0"
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ======================================================
    echo    ✅ 推送成功！
    echo ======================================================
    echo.
    echo 您的项目已成功上传到GitHub：
    echo https://github.com/lovepotatochips/HonorofKingsAgent
    echo.
    echo 按任意键退出...
    pause >nul
) else (
    echo.
    echo ======================================================
    echo    ❌ 推送失败
    echo ======================================================
    echo.
    echo 可能的原因：
    echo 1. 网络连接问题 - 请检查网络或使用VPN
    echo 2. 认证失败 - 请检查GitHub用户名和密码
    echo 3. 仓库不存在 - 请先在GitHub创建仓库
    echo.
    echo 解决方法：
    echo 1. 使用Personal Access Token代替密码（更安全）
    echo 2. 访问 https://github.com/settings/tokens 创建Token
    echo 3. 重试此命令：git push -u origin main
    echo.
    echo 详细指南请查看：GITHUB_PUSH_GUIDE.md
    echo.
    echo 按任意键退出...
    pause >nul
)
