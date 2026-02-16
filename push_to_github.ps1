# GitHub推送PowerShell脚本
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "  王者荣耀智能助手 - GitHub推送工具" -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/3] 正在推送到GitHub..." -ForegroundColor Yellow
Write-Host ""

Set-Location $PSScriptRoot
$result = git push -u origin main 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "======================================================" -ForegroundColor Green
    Write-Host "  ✅ 推送成功！" -ForegroundColor Green
    Write-Host "======================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "您的项目已成功上传到GitHub：" -ForegroundColor White
    Write-Host "https://github.com/lovepotatochips/HonorofKingsAgent" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "按任意键退出..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
} else {
    Write-Host ""
    Write-Host "======================================================" -ForegroundColor Red
    Write-Host "  ❌ 推送失败" -ForegroundColor Red
    Write-Host "======================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "可能的原因：" -ForegroundColor Yellow
    Write-Host "1. 网络连接问题 - 请检查网络或使用VPN" -ForegroundColor White
    Write-Host "2. 认证失败 - 请检查GitHub用户名和密码" -ForegroundColor White
    Write-Host "3. 仓库不存在 - 请先在GitHub创建仓库" -ForegroundColor White
    Write-Host ""
    Write-Host "解决方法：" -ForegroundColor Yellow
    Write-Host "1. 使用Personal Access Token代替密码（更安全）" -ForegroundColor White
    Write-Host "2. 访问 https://github.com/settings/tokens 创建Token" -ForegroundColor Cyan
    Write-Host "3. 重试此命令：git push -u origin main" -ForegroundColor White
    Write-Host ""
    Write-Host "详细指南请查看：GITHUB_PUSH_GUIDE.md" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "按任意键退出..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}
