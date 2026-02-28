# GitHub 云同步

## 功能概述

多设备同步记忆，私有仓库存储，支持 Git 版本控制。

## 初始化

用户给 GitHub Token 后：

```bash
export GH_TOKEN="ghp_xxx"
cd ~/.persistent-memory

# 检查仓库是否存在，不存在则创建
gh repo view user/persistent-memory 2>/dev/null || \
  gh repo create persistent-memory --private --source=. --push

# 已有仓库则克隆
git clone https://ghp_xxx@github.com/user/persistent-memory.git ~/.persistent-memory
```

## 同步流程

```bash
cd ~/.persistent-memory

# 拉取远程最新
git fetch origin
git merge origin/main --no-edit

# 添加本地变更
git add -A
git commit -m "sync: $(date +%Y-%m-%d)"
git push origin main
```

## 冲突处理

**策略：本地优先 + 用户决定**

```bash
if git merge --no-commit --no-ff origin/main 2>/dev/null; then
  git commit -m "sync: merge remote"
else
  echo "⚠️ 记忆冲突，请手动解决"
  git merge --abort
fi
```

## Token 安全

```bash
# 环境变量（推荐）
export PERSISTENT_MEMORY_GH_TOKEN="ghp_xxx"

# 加密文件
echo "ghp_xxx" | gpg -c > ~/.persistent-memory/.token.gpg
```

## 定时同步

```bash
# 每小时同步
0 * * * * cd ~/.persistent-memory && \
  git fetch origin && \
  git stash && \
  git pull --rebase origin main && \
  git stash pop && \
  git add -A -u && \
  git commit -m "sync" && \
  git push origin main
```

## 敏感信息不同步

```bash
echo "SENSITIVE.md" >> ~/.persistent-memory/.gitignore
echo ".token.gpg" >> ~/.persistent-memory/.gitignore
```
