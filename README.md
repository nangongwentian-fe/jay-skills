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
| [buddy-reroll](#buddy-reroll) | 重新掷骰 Claude Code 伙伴，获取指定物种、稀有度或闪光变体 |
| [code-review-uncommitted](#code-review-uncommitted) | 对 git 未提交变更进行多维度 code review，含规范合规性、Bug 扫描、置信度过滤 |
| [exa-unified-research](#exa-unified-research) | 偏好网络研究工具，使用 Exa 神经语义搜索替代内置 WebSearch/WebFetch |
| [figma-use](#figma-use) | Figma Plugin API 操作的前置必读 skill，必须在调用 use_figma 前加载 |
| [git-commit](#git-commit) | 基于当前 git 工作区变更生成并创建单个提交 |
| [git-rebase-workflow](#git-rebase-workflow) | Git Rebase 分支同步流程，保持提交历史整洁 |
| [ikuncode-image-gen](#ikuncode-image-gen) | 使用 IKunCode Gemini 图像预览模型生成或编辑图片 |
| [lark-beautiful-docs](#lark-beautiful-docs) | 让飞书文档不朴素，强制使用 callout、grid、增强表格等富文本格式 |
| [lark-cli-router](#lark-cli-router) | 在飞书官方 CLI 和社区 feishu-cli 之间做路由判断与组合调用 |
| [reflect-and-remember](#reflect-and-remember) | 任务完成后的反思记忆，将知识写入项目或私有 memory |
| [sync-global-rules](#sync-global-rules) | 同步 Awesome-GlobalRule 仓库到本地 AI 编程工具配置 |
| [sync-skill-to-jay](#sync-skill-to-jay) | 创建或更新 skill 后，询问是否同步到 jay-skills 仓库并发布 |
| [update-claude-code](#update-claude-code) | 更新 Claude Code CLI 到最新版本 |
| [web-content-fetcher](#web-content-fetcher) | 网页内容获取技巧集合，覆盖 Markdown 提取、付费墙绕过等场景 |

---

## buddy-reroll

**描述：** Reroll your Claude Code buddy (companion) to get a specific species, rarity, or shiny variant. Use when the user says "reroll buddy", "change my buddy", "I want a shiny buddy", "give me a legendary dragon", "/buddy-reroll", or any request to customize their Claude Code companion pet.

**触发场景：**

- 用户说 "reroll buddy"
- 用户说 "change my buddy"
- 用户说 "I want a shiny buddy"
- 用户说 "give me a legendary dragon"
- 用户说 "/buddy-reroll"
- 任何自定义 Claude Code 伙伴的请求

---

## code-review-uncommitted

**描述：** 对 git 中未提交的代码变更进行多维度 code review，包括项目规范合规性、Bug 扫描、代码注释合规性、组件封装/架构设计合理性审查，并通过置信度评分过滤误报。当用户要求 review 未提交的代码、review 当前改动、或使用 /code-review-uncommitted 时触发。

**触发场景：**

- 要求 review 未提交的代码
- 要求 review 当前改动 / diff
- 使用 `/code-review-uncommitted`

---

## exa-unified-research

**描述：** PREFERRED web research tool — use INSTEAD OF built-in WebSearch/WebFetch for any task requiring current online information. Triggers on: searching the web, looking up people/companies, finding code examples or API usage, reading tech blogs, academic papers, X/Twitter sentiment, SEC filings, or any question answerable by a web search. Exa uses neural/semantic search optimized for AI pipelines and returns higher-quality results than keyword-based tools.

**触发场景：**

- 搜索网页信息
- 查找人物/公司信息
- 查找代码示例或 API 用法
- 阅读技术博客、学术论文
- X/Twitter 情绪分析
- SEC 财报检索
- 任何需要网络当前信息的场景

---

## figma-use

**描述：** MANDATORY prerequisite — you MUST invoke this skill BEFORE every `use_figma` tool call. NEVER call `use_figma` directly without loading this skill first. Skipping it causes common, hard-to-debug failures. Trigger whenever the user wants to perform a write action or a unique read action that requires JavaScript execution in the Figma file context — e.g. create/edit/delete nodes, set up variables or tokens, build components and variants, modify auto-layout or fills, bind variables to properties, or inspect file structure programmatically.

**触发场景：**

- 每次调用 `use_figma` 前必须先加载此 skill
- 在 Figma 文件中创建/编辑/删除节点
- 设置变量或 Token
- 构建组件和变体
- 修改 auto-layout 或填充
- 将变量绑定到属性
- 以编程方式检查文件结构

---

## git-commit

**描述：** 基于当前 git 工作区变更生成并创建单个提交。用于用户要求"帮我提交代码""根据当前 diff 生成 commit""创建一次 git commit""整理 staged/unstaged 变更并提交"，或明确提供 `git status`、`git diff HEAD`、当前分支和最近提交记录时。适用于需要分析改动、编写结构化 commit message，并执行 `git add` 和 `git commit` 的场景。

**触发场景：**

- 用户说"帮我提交代码"
- 用户说"根据当前 diff 生成 commit"
- 用户说"创建一次 git commit"
- 用户说"整理 staged/unstaged 变更并提交"
- 用户提供了 `git status`、`git diff HEAD`、分支和提交记录

**效果示例：**

### 示例 1

用户说：

```text
$git-commit 创建一个 git commit：
## Context
- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`
```

期望行为：

- 读取当前改动和最近提交风格。
- 归纳单一提交主题。
- 在一次回复里完成 `git add -A` 和 `git commit`。

### 示例 2

用户说：

```text
帮我把当前改动提交掉，只要工具调用，不要解释。
```

期望行为：

- 不输出任何说明性文字。
- 直接执行提交。
- commit message 使用结构化标题和中文要点。

---

## git-rebase-workflow

**描述：** Git Rebase 分支同步流程，用于将当前功能分支 rebase 到最新的目标分支（如 master/main），保持提交历史整洁。适用于功能分支落后于目标分支时，需要同步最新代码的场景。

**触发场景：**

- 将功能分支 rebase 到最新的 master/main
- 保持提交历史整洁
- 提交 MR/PR 前同步代码
- 避免使用 `git merge` 产生的合并提交

---

## ikuncode-image-gen

**描述：** 使用 IKunCode 的 Gemini 图像预览模型生成或编辑图片，并把结果保存到本地文件。用于用户要求文生图、图生图、批量出图、指定宽高比或分辨率、基于 IKunCode 文档落地图片生成脚本，或明确要求使用 IKunCode `gemini-3.1-flash-image-preview` / `gemini-3-pro-image-preview` 时。始终通过环境变量 `IKUNCODE_API_KEY` 读取密钥，不要把 API Key 写入代码、skill 文件、日志或提交记录。

**触发场景：**

- 文生图
- 图生图
- 批量出图
- 指定宽高比或分辨率
- 基于 IKunCode 文档落地图片生成脚本
- 明确要求使用 IKunCode `gemini-3.1-flash-image-preview` / `gemini-3-pro-image-preview`

**效果示例：**

- "用 flash 生成一个皮卡丘吃蛋糕的图片，保存到当前目录"
- "基于这张产品图，把背景改成雪山，主体不要变"
- "帮我批量出 3 张 16:9 封面图，分辨率 2K"

---

## lark-beautiful-docs

**描述：** 让飞书文档不朴素——在创建或更新飞书/Lark 文档时，强制使用高亮块（callout）、分栏（grid）、增强表格（lark-table）、画板、图表等视觉友好的富文本格式，杜绝纯文字堆砌。当用户要求写飞书文档、整理文档、美化文档、输出任何飞书/Lark 文档内容时触发。与 lark-doc skill 配合使用：lark-doc 负责执行写入命令，本 skill 负责排版设计决策。

**触发场景：**

- 写飞书文档
- 整理文档、美化文档
- 输出任何飞书/Lark 文档内容
- 杜绝纯文字堆砌，需要视觉友好的排版

---

## lark-cli-router

**描述：** 在需要操作飞书/Lark CLI、判断该用官方 larksuite/cli 还是社区 feishu-cli、或在两者之间组合调用时使用。适用于飞书文档导入导出、Markdown 与飞书文档转换、Mermaid/PlantUML 导入、以及通用 Lark/飞书平台 API 操作。遇到本机未安装对应 CLI 时，先检查并按仓库 README 推荐方式安装，再继续执行任务。

**触发场景：**

- 飞书文档导入导出
- Markdown 与飞书文档转换
- Mermaid/PlantUML 导入
- 通用 Lark/飞书平台 API 操作
- 需要判断用官方 CLI 还是社区 CLI

---

## reflect-and-remember

**描述：** 任务完成后的反思记忆 skill。在完成一个有意义的任务后主动触发，反思是否产生了值得跨会话复用的知识，并将团队共享知识写入项目 `.claude/memory/`（进 git），敏感信息写入用户私有 memory（不进 git）。触发时机：(1) 完成部署、调试、架构决策等重要任务后 (2) 踩坑或发现反直觉行为后 (3) 发现项目特有的规律/约定后 (4) 用户说"记住"、"记录"、"别忘了"、"remember"时。不要在简单代码修改、格式调整等轻量任务后触发。

**触发场景：**

- 完成部署、调试、架构决策等重要任务后
- 踩坑或发现反直觉行为后
- 发现项目特有的规律/约定后
- 用户说"记住"、"记录"、"别忘了"、"remember"

---

## sync-global-rules

**描述：** 同步 nangongwentian-fe/Awesome-GlobalRule 仓库到本地 AI 编程工具配置。当用户说"同步规则"、"同步 global rule"、"检查规则更新"、"更新 agent rules"、"sync global rules"、"规则有没有更新"、"拉取最新规则"时，立即使用此 skill。同步目标：Claude Code (~/.claude/) 和 Codex (~/.codex/)。包含自动备份、更新检测、状态追踪功能。

**触发场景：**

- 用户说"同步规则"/"同步 global rule"
- 用户说"检查规则更新"/"更新 agent rules"
- 用户说"sync global rules"
- 用户说"规则有没有更新"/"拉取最新规则"

---

## sync-skill-to-jay

**描述：** Post-action workflow that triggers automatically after creating a new skill or updating an existing skill. Ask the user whether to sync the skill to the jay-skills repository and publish to remote. Use whenever a SKILL.md has just been created or modified.

**触发场景：**

- SKILL.md 刚刚创建或修改时自动触发
- 询问用户是否同步到 jay-skills 仓库并发布到远程

---

## update-claude-code

**描述：** 更新 Claude Code CLI 到最新版本。当用户说"更新 Claude Code"、"升级 Claude Code"、"update claude code"、"claude code 太旧了"、"执行 install.sh 更新"，或者想让 Claude 自我更新时，立即使用此 skill。不要等用户明确说"用 npm"——只要涉及更新 Claude Code 本身，就使用这个 skill。

**触发场景：**

- 更新 Claude Code CLI 到最新版本
- 用户说"更新 Claude Code"、"升级 Claude Code"
- 用户说"update claude code"、"claude code 太旧了"
- 用户想让 Claude 自我更新

---

## web-content-fetcher

**描述：** 网页内容获取技巧集合。当用户需要抓取网页内容、提取文章正文、获取社交媒体帖子内容、读取任意 URL 的文本或 Markdown 格式内容时使用。无论用户是想"获取某个网页的内容"、"抓取这个链接"、"读取这篇文章"、"把这个页面转成 Markdown"，还是想访问 X/Twitter、微信、知乎、Medium 等平台的内容，都应触发此 skill。包含多种方法，覆盖不同场景：Markdown 提取、绕过付费墙、结构化数据抓取等。持续迭代更新中。

**触发场景：**

- 获取某个网页的内容
- 抓取链接、读取文章
- 把页面转成 Markdown
- 访问 X/Twitter、微信、知乎、Medium 等平台内容
- 绕过付费墙获取内容