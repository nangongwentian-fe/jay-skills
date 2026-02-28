---
name: persistent-memory
description: |
  跨会话的长期记忆系统。让 AI 记住账号、配置、技术发现、项目背景等重要信息。
  适用对象：Claude Code、Codex、Open Code 等 AI 编程工具。
  触发：用户说"记住"；问"之前"；检测到敏感信息；会话结束。
---

# Persistent Memory

## Quick Start

```bash
# 初始化
mkdir -p ~/.persistent-memory/memory
cat > ~/.persistent-memory/MEMORY.md << 'EOF'
# 长期记忆
## 关于用户
- **名字**: [用户名]
## 已完成任务
## 技术知识
## 待完成
EOF
```

## 核心原则

1. **用户说"记住" = 立刻写**
2. **自动检测敏感信息，主动提示**
3. **定期整理**：合并到 MEMORY.md
4. **安全**：不记录真实密码、密钥

## 触发场景

- 用户说"记住xxx"
- 用户问"之前怎样"
- 检测到 API key、账号
- 会话结束

## 文件结构

```
~/.persistent-memory/
├── MEMORY.md           # 长期记忆
├── memory/             # 每日日记
│   └── YYYY-MM-DD.md
├── SENSITIVE.md        # 敏感信息（可选）
└── HEARTBEAT.md        # 心跳清单
```

## 会话开始

```bash
cat ~/.persistent-memory/MEMORY.md
cat ~/.persistent-memory/memory/$(date +%Y-%m-%d).md 2>/dev/null
```

## 记住信息

```bash
# 长期 → MEMORY.md
echo "- 2026-02-28: 新记录" >> ~/.persistent-memory/MEMORY.md

# 日常 → memory/YYYY-MM-DD.md
echo "### 今日" >> ~/.persistent-memory/memory/$(date +%Y-%m-%d).md
```

---

## 更多内容

- **详细工作流**: See [references/workflow.md](references/workflow.md)
- **GitHub 云同步**: See [references/sync.md](references/sync.md)
- **命令参考**: See [references/commands.md](references/commands.md)
- **兼容 Claude Code**: See [references/migration.md](references/migration.md)
