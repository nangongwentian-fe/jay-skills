---
name: persistent-memory
description: |
  跨会话的长期记忆系统。让 AI 记住账号、配置、技术发现、项目背景等重要信息，像人一样累积经验。
  触发场景：用户说"记住"/"记录"；用户问"之前"/"上次"；获取到重要信息；会话结束；收到 flush 信号。
---

# Persistent Memory

## 概述

基于文件的多层记忆系统，让 AI 具备长期记忆能力。每次会话开始时自动读取记忆中相关信息，工作过程中主动记录新知识。

## 存储位置

通用记忆文件（适用于任何 AI Agent 框架）：

```
~/.persistent-memory/
├── SOUL.md           # AI 自身身份定义（性格、说话方式）
├── USER.md           # 用户信息（名字、时区、偏好）
├── IDENTITY.md       # 身份标识（名字、emoji、人设）
├── AGENTS.md         # AI 工作规范（行为准则、工具使用）
├── MEMORY.md         # 长期记忆（精选持久信息）
├── TOOLS.md          # 本地工具配置（SSH、相机、语音等）
├── HEARTBEAT.md      # 心跳检查清单
└── memory/
    └── YYYY-MM-DD.md # 每日工作日志
```

## 文件说明

### SOUL.md - 核心身份
定义 AI 的核心价值观和行为准则：
- 真正有用而非表演式帮助
- 可以有观点和偏好
- 保守外部动作，勇敢内部行动
- 记住是客人，要尊重隐私

### USER.md - 用户画像
记录用户的基本信息：
- 名字、称呼方式
- 语言、时区
- 偏好、习惯

### IDENTITY.md - 人设
具体的人格化定义：
- 名字、emoji
- 性格、说话风格
- 头像

### AGENTS.md - 工作规范
AI 的行为准则和工具使用指南：
- 每会话必读文件清单
- 记忆系统说明
- 群聊礼仪
- 心跳使用指南

### MEMORY.md - 长期记忆
精选的持久信息：
- 已完成任务
- 技术知识
- 待办事项
- 重要账号

### TOOLS.md - 工具配置
本地环境的具体配置：
- 相机名称、SSH 主机
- TTS 语音偏好
- 设备别名

### memory/YYYY-MM-DD.md - 每日日记
每天的原始工作日志：
- 项目进展
- 学到的新东西
- 遇到的问题

## 触发场景（必须激活）

- 用户说"记住xxx"、"记录下来"
- 用户问"之前怎样"、"上次那个"
- 获取到账号、配置、技术发现、项目背景
- 完成重要任务或重大发现
- 会话结束有新内容
- 收到 flush/整理记忆信号

## 工作流程

### 1. 会话开始（自动）

按顺序读取：
```bash
# 1. 核心身份
cat ~/.persistent-memory/SOUL.md

# 2. 用户信息
cat ~/.persistent-memory/USER.md

# 3. 身份定义
cat ~/.persistent-memory/IDENTITY.md

# 4. 长期记忆
cat ~/.persistent-memory/MEMORY.md

# 5. 今日和昨日日记
cat ~/.persistent-memory/memory/$(date +%Y-%m-%d).md 2>/dev/null
cat ~/.persistent-memory/memory/$(date -d "yesterday" +%Y-%m-%d).md 2>/dev/null
```

### 2. 记住信息

**长期信息 → MEMORY.md**
```bash
echo "## 已完成任务" >> ~/.persistent-memory/MEMORY.md
echo "- 2026-02-28: 安装了 Agent Reach" >> ~/.persistent-memory/MEMORY.md
```

**用户信息 → USER.md**
```bash
echo "- **新信息**: 具体内容" >> ~/.persistent-memory/USER.md
```

**日常细节 → memory/YYYY-MM-DD.md**
```bash
DATE=$(date +%Y-%m-%d)
echo "### 新学到" >> ~/.persistent-memory/memory/$DATE.md
echo "- fxtwitter API 可获取推文完整内容" >> ~/.persistent-memory/memory/$DATE.md
```

### 3. 搜索记忆

```bash
grep -ri "关键词" ~/.persistent-memory/
ls -t ~/.persistent-memory/memory/ | head -7
```

### 4. 整理记忆（定期）

- 周期性回顾近期日记
- 将重要内容合并到 MEMORY.md
- 删除过时信息

## 核心原则

1. **用户说"记住" = 立刻写**，不问
2. **不同类型信息写入不同文件**
3. **定期整理**：每周或每次心跳时合并到 MEMORY.md
4. **安全**：不记录真实密码、银行卡等敏感信息
5. **每会话必读**：SOUL.md + USER.md + IDENTITY.md + MEMORY.md

## 与 AI 集成

在项目的 AGENTS.md 添加：

```markdown
## 记忆（每会话必读）

1. **SOUL.md** — 我是谁（核心身份）
2. **USER.md** — 用户是谁
3. **IDENTITY.md** — 人设定义
4. **MEMORY.md** — 长期记忆
5. **memory/YYYY-MM-DD.md** — 今日日记

存储位置: ~/.persistent-memory/

用户说"记住"时写入对应文件。
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

cat > ~/.persistent-memory/SOUL.md << 'EOF'
# SOUL.md - 谁是我

核心价值观和行为准则。
EOF

cat > ~/.persistent-memory/USER.md << 'EOF'
# USER.md - 用户信息

用户的基本信息。
EOF

cat > ~/.persistent-memory/IDENTITY.md << 'EOF'
# IDENTITY.md - 身份定义

名字、emoji、人设。
EOF
```
