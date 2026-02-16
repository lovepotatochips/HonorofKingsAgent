# GitHub上传操作指南

由于网络连接问题，建议您手动执行以下步骤将项目推送到GitHub：

## 方式一：使用Git Bash（推荐）

```bash
# 1. 进入项目目录
cd d:/project/HonorofKingsAgent

# 2. 添加远程仓库（如果还没有添加）
git remote add origin https://github.com/lovepotatochips/HonorofKingsAgent.git

# 3. 推送到GitHub
git push -u origin main
```

如果提示需要认证，GitHub会要求您：
- 输入GitHub用户名：`lovepotatochips`
- 输入密码或Personal Access Token

## 方式二：使用Personal Access Token（更安全）

### 1. 创建Personal Access Token
1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 设置token名称（如：HonorofKingsAgent）
4. 勾选权限：`repo`（完整仓库访问权限）
5. 点击生成并**复制token**（只显示一次）

### 2. 使用Token推送
```bash
# 使用token代替密码
git push -u origin main
# 用户名：lovepotatochips
# 密码：粘贴刚才复制的token
```

## 方式三：使用SSH密钥（长期推荐）

### 1. 生成SSH密钥
```bash
ssh-keygen -t ed25519 -C "lovepotatochips@github.com"
```

### 2. 添加SSH密钥到GitHub
1. 复制公钥：`cat ~/.ssh/id_ed25519.pub`
2. 访问：https://github.com/settings/keys
3. 点击 "New SSH key"
4. 粘贴公钥并保存

### 3. 使用SSH推送
```bash
# 修改远程仓库地址为SSH格式
git remote set-url origin git@github.com:lovepotatochips/HonorofKingsAgent.git

# 推送
git push -u origin main
```

## 检查当前状态

```bash
# 查看远程仓库
git remote -v

# 查看分支
git branch -a

# 查看提交历史
git log --oneline
```

## 常见问题

### Q: 推送时提示 "connection was reset"
A: 网络问题，请重试或使用VPN

### Q: 提示 "Authentication failed"
A: 用户名或密码错误，请检查或使用Personal Access Token

### Q: 提示 "Repository not found"
A: 仓库地址错误或未创建仓库，请先在GitHub创建仓库

### Q: 提示 "remote already exists"
A: 远程仓库已存在，可以使用：
```bash
git remote set-url origin https://github.com/lovepotatochips/HonorofKingsAgent.git
```

## 完成后

推送成功后，您可以访问：
https://github.com/lovepotatochips/HonorofKingsAgent

查看您的项目！
