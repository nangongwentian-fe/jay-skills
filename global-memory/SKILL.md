---
name: persistent-memory
description: |
  跨会话的长期记忆系统，让 AI 记住重要信息、工作进展、技术知识、账号配置等。
  当用户说"记住"、"记录"、"memory"、"记忆"时必须使用此 skill。
  适用于：记录账号 token、记录项目背景、记录技术发现、回顾之前工作、搜索历史记忆。
  使用此 skill 来实现类似人类的记忆能力——重要信息长期记住，日常细节按需回忆。
---

# Persistent Memory - 长期记忆系统

## 核心理念

AI 没有记忆 = 每次从头开始
AI 有记忆 = 累积经验，理解上下文，记住偏好

**这个 skill 复制了小龙虾的记忆工作方式。**

## 工作流程

### 1. 会话开始时（自动执行）

```
读取以下文件：
1. LONGTERM.md - 长期记忆
2. 当日 daily/YYYY-MM-DD.md - 如果存在
3. 昨日 daily/YYYY-MM-DD.md - 快速了解最近在做什么
```

### 2. 什么情况会记忆

| 触发条件 | 写入位置 | 示例 |
|---------|---------|------|
| 用户说"记住" | LONGTERM.md | "记住我的 GitHub token 是 xxx" |
| 重要技术发现 | daily/ | "学会了用 fxtwitter API 获取 X 内容" |
| 完成重要任务 | daily/ | "配置好了 nginx" |
| 用户问"之前" | 搜索记忆 | "之前那个问题怎么解决的？" |
| 会话结束有新内容 | 询问是否保存 | "需要记住这个吗？" |

### 3. 写入格式

**LONGTERM.md 格式**：
```markdown
# 长期记忆

## 账号
- **GitHub**: ghp_xxx

## 技术知识
- **X内容获取**: 用 api.fxtwitter.com/status/{id}

## 项目
- **文杰的项目**: xxx

## 偏好
- 语言: 中文
```

**daily/YYYY-MM-DD.md 格式**：
```markdown
# 2026-02-28 工作记录

## 完成
- 获取了 X.com 文章内容

## 发现
- fxtwitter API 比 oembed 更好用

## 待办
- 优化成本趋势图
```

### 4. 搜索记忆

当用户问"之前"、"以前"、"上次"时：
```bash
# 搜索关键词
grep -ri "关键词" ~/.claude/memory/

# 或读取最近几天
ls -t ~/.claude/memory/daily/ | head -7
```

## 文件结构

```
~/.claude/memory/
├── LONGTERM.md          # 长期记忆（精简，核心信息）
└── daily/
    ├── 2026-02-27.md   # 每日详细记录
    ├── 2026-02-28.md
    └── ...
```

## 初始化

```bash
# 首次使用
mkdir -p ~/.claude/memory/daily

# 创建 LONGTERM.md
cat > ~/.claude/memory/LONGTERM.md << 'EOF'
# 长期记忆

## 账号

## 技术知识

## 项目

## 偏好
EOF

# 创建今日记录
cat > ~/.claude/memory/daily/$(date +%Y-%m-%d).md << EOF
# $(date +%Y-%m-%d) 工作记录

## 完成

## 发现

## 待办
EOF
```

## 与 AI 工作流集成

### 在 CLAUDE.md 中添加
```
## 记忆系统
每次会话开始时：
1. cat ~/.claude/memory/LONGTERM.md
2. cat ~/.claude/memory/daily/$(date +%Y-%m-%d).md 2>/dev/null || true

用户说"记住"时：
- 追加到 ~/.claude/memory/LONGTERM.md（重要信息）
- 或 ~/.claude/memory/daily/$(date +%Y-%m-%d).md（日常工作）

每月整理：
- 将 daily 中的重要内容迁移到 LONGTERM.md
```

### 在 settings.json 中配置
```json
{
  "preRunPrompt": "先读取记忆：cat ~/.claude/memory/LONGTERM.md && cat ~/.claude/memory/daily/$(date +%Y-%m-%d).md"
}
```

## 关键原则

1. **用户说"记住" = 立即执行**：不要问，直接写
2. **长期 vs 短期**：配置/偏好 → LONGTERM；工作细节 → daily
3. **可检索**：用关键词组织，grep 能搜到
4. **定期整理**：每月把 daily 重要内容合并到 LONGTERM
5. **安全**：不记录真实密码、银行卡

## 与其他 AI 工具共享

```bash
# Claude Code 和 Codex 共享
ln -s ~/.claude/memory ~/.codex/memory
```
