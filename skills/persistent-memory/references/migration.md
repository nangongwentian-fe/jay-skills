# 兼容 Claude Code

Claude Code 使用 `~/.claude/memory/` 目录。

## 迁移方案

### 方案一：软链接（推荐）

```bash
ln -s ~/.claude/memory ~/.persistent-memory
```

优点：两边同步，零存储

### 方案二：复制

```bash
cp -r ~/.claude/memory/* ~/.persistent-memory/
```

优点：独立存储

### 方案三：合并

```bash
# 保留两边
cat ~/.claude/memory/LONGTERM.md >> ~/.persistent-memory/MEMORY.md
cp ~/.claude/memory/daily/*.md ~/.persistent-memory/memory/
```

## 目录对照

| Claude Code | Persistent Memory |
|-------------|------------------|
| ~/.claude/memory/LONGTERM.md | ~/.persistent-memory/MEMORY.md |
| ~/.claude/memory/daily/ | ~/.persistent-memory/memory/ |
