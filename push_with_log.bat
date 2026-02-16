@echo off
chcp 65001 >nul
set LOG_FILE=git_push_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log

echo ======================================================
echo    王者荣耀智能助手 - GitHub推送工具（带日志）
echo ======================================================
echo.
echo 日志文件：git_push.log
echo 开始时间：%date% %time%
echo.

cd /d "%~dp0"

echo [1/3] 检查Git状态...
git status >> git_push.log 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git状态检查失败
    goto :error
)
echo ✅ Git状态检查完成
echo.

echo [2/3] 检查远程仓库...
git remote -v >> git_push.log 2>&1
if %errorlevel% neq 0 (
    echo ❌ 远程仓库检查失败
    goto :error
)
echo ✅ 远程仓库检查完成
echo.

echo [3/3] 推送到GitHub...
echo 正在推送，请稍候...
echo.
git push -u origin main >> git_push.log 2>&1

if %errorlevel% equ 0 (
    echo.
    echo ======================================================
    echo    ✅ 推送成功！
    echo ======================================================
    echo.
    echo 您的项目已成功上传到GitHub：
    echo https://github.com/lovepotatochips/HonorofKingsAgent
    echo.
    echo 日志已保存到：git_push.log
    echo 完成时间：%date% %time%
    echo.
    pause
    exit /b 0
) else (
    :error
    echo.
    echo ======================================================
    echo    ❌ 推送失败
    echo ======================================================
    echo.
    echo 详细错误信息已保存到：git_push.log
    echo.
    echo 常见错误及解决方法：
    echo.
    echo 1. 认证失败
    echo    解决：使用Personal Access Token代替密码
    echo    地址：https://github.com/settings/tokens
    echo.
    echo 2. 网络连接失败
    echo    解决：检查网络连接或使用VPN
    echo.
    echo 3. 仓库不存在
    echo    解决：确认GitHub上已创建仓库
    echo.
    echo 查看完整日志：notepad git_push.log
    echo.
    pause
    exit /b 1
)
