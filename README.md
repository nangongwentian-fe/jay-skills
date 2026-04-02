# Jay Skills

> Jay 的 AI Agent Skills 集合，适用于 Claude Code / Codex 等 AI 编程工具。

## 安装

```bash
# 安装全部 skills
npx skills add https://github.com/nangongwentian-fe/jay-skills -g -y -a claude-code codex

# 安装单个 skill
npx skills add https://github.com/nangongwentian-fe/jay-skills --skill <skill-name> -g -y
```

## Skills 列表

| Skill | 描述 |
|-------|------|
| [buddy-reroll](#buddy-reroll) | 重新随机你的 Claude Code 伙伴（种类、稀有度、闪光） |
| [code-review-uncommitted](#code-review-uncommitted) | 多维度 code review 未提交变更，含置信度评分 |
| [exa-unified-research](#exa-unified-research) | 优先使用 Exa 进行高质量网络检索，替代内置 WebSearch |
| [figma-use](#figma-use) | 调用 Figma Plugin API 前的必备 skill，含全量规则与参考文档 |
| [git-rebase-workflow](#git-rebase-workflow) | 将功能分支 rebase 到目标分支，保持提交历史整洁 |
| [lark-beautiful-docs](#lark-beautiful-docs) | 让飞书文档好看——callout、分栏、增强表格，拒绝纯文字堆砌 |
| [lark-cli-router](#lark-cli-router) | 飞书 CLI 路由：判断用官方 larksuite/cli 还是社区 feishu-cli |
| [persistent-memory](#persistent-memory) | 跨会话记忆协议，多 AI 工具共享同一套记忆系统 |
| [reflect-and-remember](#reflect-and-remember) | 任务完成后自动反思，将有价值的知识写入持久记忆 |
| [sync-global-rules](#sync-global-rules) | 同步 Awesome-GlobalRule 仓库到本地 AI 工具配置 |
| [sync-skill-to-jay](#sync-skill-to-jay) | 创建或更新 skill 后，一键同步到 jay-skills 并发布 |
| [update-claude-code](#update-claude-code) | 更新 Claude Code CLI 到最新版本 |
| [web-content-fetcher](#web-content-fetcher) | 抓取网页内容，支持付费墙绕过和结构化数据提取 |

---

## buddy-reroll

**描述：** 重新随机你的 Claude Code 伙伴（companion），可指定种类、稀有度或闪光变体。

**触发场景：**
- "reroll buddy"、"change my buddy"、"I want a shiny buddy"
- "give me a legendary dragon"、"/buddy-reroll"
- 任何自定义 Claude Code 伙伴宠物的请求

---

## code-review-uncommitted

**描述：** 对 git 中未提交的代码变更进行多维度 code review。

**触发场景：**
- 用户要求 review 未提交的代码或当前改动
- 使用 `/code-review-uncommitted` 命令

**检查维度：** 项目规范合规性、Bug 扫描、代码注释合规性、组件封装/架构设计合理性，并通过置信度评分过滤误报。

---

## exa-unified-research

**描述：** 优先使用 Exa 神经语义搜索替代内置 WebSearch/WebFetch，获得更高质量的检索结果。

**触发场景：**
- 搜索网络、查找人物/公司信息
- 查找代码示例或 API 用法
- 阅读技术博客、学术论文、X/Twitter 动态
- 任何可通过网络搜索回答的问题

---

## figma-use

**描述：** 调用 `use_figma` 工具前的**必备前置 skill**，包含 Figma Plugin API 完整规则、陷阱列表和参考文档。

**触发场景：**
- 在 Figma 文件中创建/编辑/删除节点
- 设置变量（variables）或 token
- 构建组件和 variant
- 修改 auto-layout、填充色（fills）
- 绑定变量到节点属性
- 以编程方式检查文件结构

**重要：** 跳过此 skill 直接调用 `use_figma` 会导致常见且难以调试的失败，请务必在每次 `use_figma` 调用前加载。

**参考文档覆盖：** gotchas、常用 pattern、Plugin API 类型定义（.d.ts）、组件/变量/文本/效果样式 pattern、Design System 集成指南。

---

## git-rebase-workflow

**描述：** Git Rebase 分支同步流程，将当前功能分支 rebase 到最新目标分支（如 master/main）。

**触发场景：**
- 功能分支落后于目标分支，需要同步最新代码
- 希望保持整洁线性提交历史

---

## lark-beautiful-docs

**描述：** 在创建或更新飞书/Lark 文档时，强制使用视觉友好的富文本格式，杜绝纯文字堆砌。

**触发场景：**
- 创建、整理、美化飞书文档
- 输出任何飞书/Lark 文档内容

**可用格式：** 高亮块（callout）、分栏（grid）、增强表格（lark-table）、画板、图表。与 `lark-doc` skill 配合使用。

---

## lark-cli-router

**描述：** 飞书/Lark CLI 路由，判断该用官方 `larksuite/cli` 还是社区 `feishu-cli`，或组合调用两者。

**触发场景：**
- 飞书文档导入导出、Markdown 与飞书文档互转
- Mermaid/PlantUML 导入
- 通用 Lark/飞书平台 API 操作

---

## persistent-memory

**描述：** 通用跨会话记忆协议，让 Claude Code / Cursor / Aider / Cline / Codex / Trae / OpenCode 共享同一套记忆系统。

**触发场景：**
- 用户说"记住"、问"之前"发生的事
- 检测到敏感信息、会话结束

**能力：** 智能分类、FSRS 衰减、月度压缩、多层检索。

---

## reflect-and-remember

**描述：** 任务完成后的反思记忆 skill，主动将有价值的知识写入持久记忆。

**触发场景：**
- 完成部署、调试、架构决策等重要任务后
- 踩坑或发现反直觉行为后
- 用户说"记住"、"记录"、"别忘了"

**写入规则：** 团队共享知识写入项目 `.claude/memory/`（进 git），敏感信息写入用户私有 memory（不进 git）。

---

## sync-global-rules

**描述：** 同步 `nangongwentian-fe/Awesome-GlobalRule` 仓库到本地 AI 编程工具配置。

**触发场景：**
- "同步规则"、"检查规则更新"、"sync global rules"

**同步目标：** Claude Code (`~/.claude/`) 和 Codex (`~/.codex/`)，含自动备份、更新检测。

---

## sync-skill-to-jay

**描述：** 创建或更新 skill 后，一键同步到 jay-skills 仓库并发布到 GitHub。

**触发场景：**
- 任何 SKILL.md 刚被创建或修改后自动触发

**流程：** 复制文件 → 更新 README → commit + push → 重装为 skills 框架管理版本。

---

## update-claude-code

**描述：** 更新 Claude Code CLI 到最新版本。

**触发场景：**
- "更新 Claude Code"、"升级 Claude Code"、"update claude code"
- "claude code 太旧了"、任何让 Claude 自我更新的请求

---

## web-content-fetcher

**描述：** 网页内容获取技巧集合，支持付费墙绕过、结构化数据提取。

**触发场景：**
- 抓取网页内容、提取文章正文
- 获取 X/Twitter、微信、知乎、Medium 等平台内容
- "获取某个网页的内容"、"把这个页面转成 Markdown"
