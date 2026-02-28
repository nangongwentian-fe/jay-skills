---
name: persistent-memory
description: |
  跨会话的长期记忆系统。让 AI 记住账号、配置、技术发现、项目背景等重要信息，像人一样累积经验。
  适用对象：Claude Code、Codex、Open Code 等 AI 编程工具（它们不具备完整的记忆系统）。
  触发场景：用户说"记住"/"记录"；用户问"之前"/"上次"；获取到重要信息；自动检测到敏感信息。
---

# Persistent Memory

## 概述

基于文件的多层记忆系统，让 AI 具备长期记忆能力。每次会话开始时自动读取记忆中相关信息，工作过程中主动记录新知识。

## 存储位置

```
~/.persistent-memory/          # 推荐目录
~/.claude/memory/             # 兼容 Claude Code
~/.claude/memory/LONGTERM.md  # Claude Code 长期记忆
~/.claude/memory/daily/       # Claude Code 每日日记
```

## 文件结构

```
~/.persistent-memory/
├── MEMORY.md           # 长期记忆（精选持久信息）
├── memory/
│   └── YYYY-MM-DD.md   # 每日工作日志
├── SENSITIVE.md        # 敏感信息清单（可选加密）
└── HEARTBEAT.md        # 心跳检查清单
```

## 触发场景（必须激活）

### 显式触发
- 用户说"记住xxx"、"记录下来"
- 用户问"之前怎样"、"上次那个"
- 完成重要任务或重大发现
- 会话结束有新内容
- 收到 flush/整理记忆信号

### 自动触发（重要！）
检测到以下信息时，**主动提示用户**是否记录：
- API key、token、账号密码（不管是否打码）
- 项目背景、技术决策
- 用户偏好、习惯
- 重要联系人、联系方式
- 配置变更、环境差异

## 工作流程

### 1. 会话开始（自动）

```bash
# 读取长期记忆
cat ~/.persistent-memory/MEMORY.md

# 读取今日和昨日
cat ~/.persistent-memory/memory/$(date +%Y-%m-%d).md 2>/dev/null
cat ~/.persistent-memory/memory/$(date -d "yesterday" +%Y-%m-%d).md 2>/dev/null
```

### 2. 记住信息

**长期信息 → MEMORY.md**
```bash
echo "## 已完成任务" >> ~/.persistent-memory/MEMORY.md
echo "- 2026-02-28: 安装了 Agent Reach" >> ~/.persistent-memory/MEMORY.md
```

**日常细节 → memory/YYYY-MM-DD.md**
```bash
DATE=$(date +%Y-%m-%d)
echo "### 新学到" >> ~/.persistent-memory/memory/$DATE.md
echo "- fxtwitter API 可获取推文完整内容" >> ~/.persistent-memory/memory/$DATE.md
```

### 3. 自动检测敏感信息

检测到敏感信息时，提示用户：
```
⚠️ 检测到敏感信息 [API Key/Token/账号]，是否需要记录到 SENSITIVE.md？（建议只记录账号名，不记录实际密钥）
```

### 4. 搜索记忆

```bash
grep -ri "关键词" ~/.persistent-memory/
ls -t ~/.persistent-memory/memory/ | head -7
```

### 5. 整理记忆（定期）

- 周期性（每次心跳或每周）回顾近期日记
- 将重要内容合并到 MEMORY.md
- 删除 MEMORY.md 中过时信息

## 敏感信息安全

### 绝对不记录
- 真实密码
- 银行卡号
- API 真实密钥（可记录账号名）
- 私人隐私

### 可以记录
- 账号名/ID
- 配置项名称
- 技术方案
- 项目背景
- 网址/链接

### 敏感信息检测规则
```bash
# 检测可能敏感的字符串
grep -E "(sk-|ghp_|eyJh|bearer|password|secret|key)" ~/.persistent-memory/
```

## 兼容 Claude Code

Claude Code 使用 `~/.claude/memory/`，可以创建软链接：

```bash
# 方案一：软链接（推荐）
ln -s ~/.claude/memory ~/.persistent-memory

# 方案二：复制
cp -r ~/.claude/memory/* ~/.persistent-memory/
```

## 核心原则

1. **用户说"记住" = 立刻写**，不问
2. **自动检测敏感信息，主动提示**
3. **定期整理**：每周或每次心跳时合并到 MEMORY.md
4. **安全第一**：不记录真实密码、密钥
5. **向后兼容**：支持 Claude Code 目录

## 与其他 Skill 联动

### 语义搜索（与 Exa 联动）

利用 Exa MCP 实现语义搜索记忆：

```bash
# 安装 exa-web-search-free skill 后可用
mcporter call 'exa.get_code_context_exa(query: "上次配置的 Twitter", tokensNum: 1000)'
```

### 定期备份（与 cron 联动）

使用 cron 定期导出记忆：

```bash
# 每周日导出记忆
0 0 * * 0 tar -czf ~/memory-backup-$(date +\%Y-\%m-\%d).tar.gz ~/.persistent-memory/
```

## 导出/导入

### 导出所有记忆

```bash
# 打包所有记忆
tar -czf memory-backup.tar.gz ~/.persistent-memory/

# 导出为单文件（可编辑）
cat ~/.persistent-memory/MEMORY.md > memory-export.txt
cat ~/.persistent-memory/memory/*.md >> memory-export.txt
```

### 导入备份

```bash
# 解压备份
tar -xzf memory-backup.tar.gz -C ~/

# 选择性导入（合并）
cat memory-export.txt | while read line; do
  # 检查是否已存在
  grep -q "$line" ~/.persistent-memory/MEMORY.md || echo "$line" >> ~/.persistent-memory/MEMORY.md
done
```

### 迁移指南（从 Claude Code 迁移）

```bash
# 方案一：软链接（推荐，保持同步）
ln -s ~/.claude/memory ~/.persistent-memory

# 方案二：复制（独立备份）
cp -r ~/.claude/memory/* ~/.persistent-memory/

# 方案三：合并（保留两边）
cat ~/.claude/memory/LONGTERM.md >> ~/.persistent-memory/MEMORY.md
cp ~/.claude/memory/daily/*.md ~/.persistent-memory/memory/
```

## 与 AI 集成

在项目的 AGENTS.md 或 CLAUDE.md 添加：

```markdown
## 记忆

- 长期: ~/.persistent-memory/MEMORY.md
- 每日: ~/.persistent-memory/memory/$(date +%Y-%m-%d).md
- 敏感: ~/.persistent-memory/SENSITIVE.md
- 会话开始读取，用户说"记住"时写入
- 检测到敏感信息时主动提示用户
```

## 初始化

```bash
mkdir -p ~/.persistent-memory/memory
cat > ~/.persistent-memory/MEMORY.md << 'EOF'
# MEMORY.md - 长期记忆

## 关于我
- **名字**: [AI名字]
- **性格**: [性格描述]

## 关于用户
- **名字**: [用户名]
- **语言**: [语言]
- **时区**: [时区]

## 已完成任务

## 技术知识

## 待完成

## 记住的账号
EOF

cat > ~/.persistent-memory/SENSITIVE.md << 'EOF'
# SENSITIVE.md - 敏感信息清单

只记录账号名，不记录真实密钥。

## 账号
- **GitHub**: [账号名]
- **API**: [服务名]-[环境]

## 重要提示
- 不记录真实密码
- 不记录真实 token
- 只记录账号名/标识符
EOF
```
