---
name: persistent-memory
description: |
  跨会话的长期记忆系统。让 AI 记住账号、配置、技术发现、项目背景等，重要信息长期记住，日常细节按需回忆。
  必须使用当：用户说"记住"、"记录"；用户问"之前"、"上次"；获取到重要信息。
  效果：不用每次从头开始，像人一样累积经验。
---

# Persistent Memory

## 触发场景（必须激活）

- 用户说"记住xxx"、"记录下来"
- 用户问"之前怎样"、"上次那个"
- 获取到账号、配置、技术发现、项目背景
- 会话结束有新内容
- 收到 flush/整理记忆信号

## 工作流程

### 1. 会话开始（自动）
```bash
# 读取长期记忆
cat ~/.claude/memory/LONGTERM.md

# 读取今日和昨日
cat ~/.claude/memory/daily/$(date +%Y-%m-%d).md 2>/dev/null
cat ~/.claude/memory/daily/$(date -d "yesterday" +%Y-%m-%d).md 2>/dev/null
```

### 2. 记住信息
```bash
# 账号/配置/偏好 → LONGTERM.md
echo "- **GitHub**: ghp_xxx" >> ~/.claude/memory/LONGTERM.md

# 工作细节 → daily
DATE=$(date +%Y-%m-%d)
echo "- 学会用 fxtwitter API" >> ~/.claude/memory/daily/$DATE.md
```

### 3. 搜索记忆
```bash
grep -ri "关键词" ~/.claude/memory/
# 或
ls -t ~/.claude/memory/daily/ | head -7
```

### 4. 整理记忆（定期）
把 daily 重要内容合并到 LONGTERM.md，删除过时信息。

## 文件结构
```
~/.claude/memory/
├── LONGTERM.md        # 长期：账号、技术、项目、偏好
└── daily/            # 每日工作日志
    └── YYYY-MM-DD.md
```

## 初始化
```bash
mkdir -p ~/.claude/memory/daily
cat > ~/.claude/memory/LONGTERM.md << 'EOF'
# 长期记忆
## 账号
## 技术
## 项目
## 偏好
EOF
```

## 核心原则

1. **用户说"记住" = 立刻写**，不问
2. **长期 → LONGTERM**，**日常 → daily**
3. **定期整理**：每月合并到 LONGTERM
4. **安全**：不记录真实密码、银行卡

## 与 AI 集成

在 CLAUDE.md 添加：
```
## 记忆
- 长期: ~/.claude/memory/LONGTERM.md
- 每日: ~/.claude/memory/daily/$(date +%Y-%m-%d).md
- 会话开始读取，用户说"记住"时写入
```
