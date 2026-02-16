# 检查Git状态
Write-Host "=== Git Remote ==="
git remote -v
Write-Host ""
Write-Host "=== Git Branch ==="
git branch
Write-Host ""
Write-Host "=== Git Log ==="
git log --oneline -3
