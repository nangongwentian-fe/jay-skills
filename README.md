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
| [de-gpt-ify](#de-gpt-ify) | 中文输出去黑话化，让 GPT 像人一样说中文，告别咨询黑话和 AI 味表达 |
| [exa-unified-research](#exa-unified-research) | 偏好网络研究工具，使用 Exa 神经语义搜索替代内置 WebSearch/WebFetch |
| [figma-use](#figma-use) | Figma Plugin API 操作的前置必读 skill，必须在调用 use_figma 前加载 |
| [git-commit](#git-commit) | 基于当前 git 工作区变更生成并创建单个提交 |
| [git-rebase-workflow](#git-rebase-workflow) | Git Rebase 分支同步流程，保持提交历史整洁 |
| [ikuncode-image-gen](#ikuncode-image-gen) | 使用 IKunCode Gemini 图像预览模型生成或编辑图片 |
| [lark-beautiful-docs](#lark-beautiful-docs) | 让飞书文档不朴素，强制使用 callout、grid、增强表格等富文本格式 |
| [lark-cli-router](#lark-cli-router) | 在飞书官方 CLI 和社区 feishu-cli 之间做路由判断与组合调用 |
| [reflect-and-remember](#reflect-and-remember) | 任务完成后的反思记忆，将知识写入项目或私有 memory |
| [show-dont-tell](#show-dont-tell) | 信息可视化呈现，让 GPT 优先用表格、代码块、列表呈现结构化信息 |
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

## de-gpt-ify

**描述：** 中文输出去黑话化行为准则。让 Codex/ChatGPT 的中文输出像 Claude 一样简洁、直接、自然，避免咨询黑话、网络流行语、虚假紧迫感、情感绑架等 AI 味表达。

**触发场景：**

- 用户说"讲人话""去油""去黑话""去 AI 味""别那么 GPT""正常说话"
- 用户说"这段话太 GPT 了""帮我改成人话""输出太油了"
- 模型生成中文回复时自动生效

**安装后额外步骤：**

运行安装脚本将核心规则写入 `~/.codex/AGENTS.md`（始终生效）：

```bash
~/.agents/skills/de-gpt-ify/scripts/install.sh
```

**效果示范：**

❌ GPT 式：我已经把差异**收窄**了，**根因基本坐实**，**稳稳兜住**，**落盘**之后就能**收口**了。

✅ 人话：已缩小排查范围，初步确认根因是连接池泄漏。下一步做排除验证，确认后给出结论。

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

## show-dont-tell

**描述：** 信息可视化呈现行为准则。让 GPT 在回复中优先使用表格、代码块、编号列表、树形结构等格式呈现结构化信息，而不是纯文字堆砌。与 de-gpt-ify 互补：de-gpt-ify 解决"怎么说话"，show-dont-tell 解决"怎么呈现"。

**触发场景：**

- 回复中包含对比、步骤、配置、架构等结构化信息时自动生效
- 用户说"用表格""列个表""结构化一下""可视化""更直观一点"

**安装后额外步骤：**

```bash
~/.agents/skills/show-dont-tell/scripts/install.sh
```

**效果示范：**

❌ 纯文字：Redis 支持多种数据结构包括字符串、列表、哈希、集合和有序集合，而 Memcached 只支持简单的键值对。Redis 支持数据持久化...

✅ 表格：

| 维度 | Redis | Memcached |
|------|-------|-----------|
| 数据结构 | string / list / hash / set / zset | 仅 key-value |
| 持久化 | 支持（RDB / AOF） | 不支持 |
| 线程模型 | 单线程（6.0 起 IO 多线程） | 多线程 |

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

## Skills 列表

| Skill | 描述 |
|-------|------|
| [buddy-reroll](#buddy-reroll) | > |
| [code-review-uncommitted](#code-review-uncommitted) | 对 git 中未提交的代码变更进行多维度 code review，包括项目规范合规性、Bug 扫描、代码注释合规性、组件封装/架构设计合理性审查，并通过置... |
| [de-gpt-ify](#de-gpt-ify) | 中文输出去黑话化行为准则。当模型用中文回复时自动激活，确保输出简洁、直接、自然，避免咨询黑话、网络流行语、虚假紧迫感、情感绑架等 AI 味表达。触发词：「... |
| [exa-unified-research](#exa-unified-research) | Use this skill for ANY web research task — looking up companies, finding peop... |
| [figma-use](#figma-use) | **MANDATORY prerequisite** — you MUST invoke this skill BEFORE every `use_fig... |
| [git-commit](#git-commit) | 基于当前 git 工作区变更生成并创建单个提交。用于用户要求“帮我提交代码”“根据当前 diff 生成 commit”“创建一次 git commit”“... |
| [git-rebase-workflow](#git-rebase-workflow) | Git Rebase 分支同步流程，用于将当前功能分支 rebase 到最新的目标分支（如 master/main），保持提交历史整洁。适用于功能分支落后... |
| [ikuncode-image-gen](#ikuncode-image-gen) | 使用 IKunCode 的 Gemini 图像预览模型生成或编辑图片，并把结果保存到本地文件。用于用户要求文生图、图生图、批量出图、指定宽高比或分辨率、基... |
| [lark-beautiful-docs](#lark-beautiful-docs) | 让飞书文档不朴素——在创建或更新飞书/Lark 文档时，强制使用高亮块（callout）、分栏（grid）、增强表格（lark-table）、画板、图表等... |
| [lark-cli-router](#lark-cli-router) | 在需要操作飞书/Lark CLI、判断该用官方 larksuite/cli 还是社区 feishu-cli、或在两者之间组合调用时使用。适用于飞书文档导入... |
| [progressive-disclosure-docs](#progressive-disclosure-docs) | Design, create, split, or revise Markdown/project documentation using progres... |
| [reflect-and-remember](#reflect-and-remember) | | |
| [show-dont-tell](#show-dont-tell) | 信息可视化呈现行为准则。当模型回复中包含对比、步骤、配置、架构等结构化信息时自动激活，确保优先使用表格、代码块、列表、树形结构等可视化格式，而不是纯文字堆... |
| [sync-global-rules](#sync-global-rules) | > |
| [sync-skill-to-jay](#sync-skill-to-jay) | Post-action workflow that triggers automatically after creating a new skill o... |
| [update-claude-code](#update-claude-code) | 更新 Claude Code CLI 到最新版本。当用户说"更新 Claude Code"、"升级 Claude Code"、"update claude... |
| [web-content-fetcher](#web-content-fetcher) | > |

---

## buddy-reroll

**描述：** >

**触发场景：**

- 相关任务触发

---

## code-review-uncommitted

**描述：** 对 git 中未提交的代码变更进行多维度 code review，包括项目规范合规性、Bug 扫描、代码注释合规性、组件封装/架构设计合理性审查，并通过置信度评分过滤误报。当用户要求 review 未提交的代码、review 当前改动、或使用 /code-review-uncommitted 时触发。

**触发场景：**

- 相关任务触发

---

## de-gpt-ify

**描述：** 中文输出去黑话化行为准则。当模型用中文回复时自动激活，确保输出简洁、直接、自然，避免咨询黑话、网络流行语、虚假紧迫感、情感绑架等 AI 味表达。触发词：「讲人话」「去油」「去黑话」「去 AI 味」「别那么 GPT」「正常说话」。即使没有触发词，只要模型在生成中文回复，本 skill 的规则就应当生效。也适用于用户说「这段话太 GPT 了」「帮我改成人话」「输出太油了」「说话别绕」等场景。

**触发场景：**

- 相关任务触发

---

## exa-unified-research

**描述：** Use this skill for ANY web research task — looking up companies, finding people, searching for code examples or API docs, reading tech blogs, finding academic papers, checking SEC filings or financial reports, or gauging social media sentiment. Covers any question that requires searching the internet for current information. Exa provides neural/semantic search that returns higher-quality, better-structured results than simple keyword search. Load this skill whenever the user asks you to search, research, find, look up, or investigate anything online — even if you think you can handle it with built-in search tools, this skill will produce significantly better results.

**触发场景：**

- 相关任务触发

---

## figma-use

**描述：** **MANDATORY prerequisite** — you MUST invoke this skill BEFORE every `use_figma` tool call. NEVER call `use_figma` directly without loading this skill first. Skipping it causes common, hard-to-debug failures. Trigger whenever the user wants to perform a write action or a unique read action that requires JavaScript execution in the Figma file context — e.g. create/edit/delete nodes, set up variables or tokens, build components and variants, modify auto-layout or fills, bind variables to properties, or inspect file structure programmatically.

**触发场景：**

- 相关任务触发

---

## git-commit

**描述：** 基于当前 git 工作区变更生成并创建单个提交。用于用户要求“帮我提交代码”“根据当前 diff 生成 commit”“创建一次 git commit”“整理 staged/unstaged 变更并提交”，或明确提供 `git status`、`git diff HEAD`、当前分支和最近提交记录时。适用于需要分析改动、编写结构化 commit message，并执行 `git add` 和 `git commit` 的场景。

**触发场景：**

- 相关任务触发

---

## git-rebase-workflow

**描述：** Git Rebase 分支同步流程，用于将当前功能分支 rebase 到最新的目标分支（如 master/main），保持提交历史整洁。适用于功能分支落后于目标分支时，需要同步最新代码的场景。

**触发场景：**

- 相关任务触发

---

## ikuncode-image-gen

**描述：** 使用 IKunCode 的 Gemini 图像预览模型生成或编辑图片，并把结果保存到本地文件。用于用户要求文生图、图生图、批量出图、指定宽高比或分辨率、基于 IKunCode 文档落地图片生成脚本，或明确要求使用 IKunCode `gemini-3.1-flash-image-preview` / `gemini-3-pro-image-preview` 时。始终通过环境变量 `IKUNCODE_API_KEY` 读取密钥，不要把 API Key 写入代码、skill 文件、日志或提交记录。

**触发场景：**

- 相关任务触发

---

## lark-beautiful-docs

**描述：** 让飞书文档不朴素——在创建或更新飞书/Lark 文档时，强制使用高亮块（callout）、分栏（grid）、增强表格（lark-table）、画板、图表等视觉友好的富文本格式，杜绝纯文字堆砌。当用户要求写飞书文档、整理文档、美化文档、输出任何飞书/Lark 文档内容时触发。与 lark-doc skill 配合使用：lark-doc 负责执行写入命令，本 skill 负责排版设计决策。

**触发场景：**

- 相关任务触发

---

## lark-cli-router

**描述：** 在需要操作飞书/Lark CLI、判断该用官方 larksuite/cli 还是社区 feishu-cli、或在两者之间组合调用时使用。适用于飞书文档导入导出、Markdown 与飞书文档转换、Mermaid/PlantUML 导入、以及通用 Lark/飞书平台 API 操作。遇到本机未安装对应 CLI 时，先检查并按仓库 README 推荐方式安装，再继续执行任务。

**触发场景：**

- 相关任务触发

---

## progressive-disclosure-docs

**描述：** Design, create, split, or revise Markdown/project documentation using progressive disclosure so agents and humans can find the right level of detail without context bloat. Use when writing docs, README files, runbooks, architecture notes, deployment guides, troubleshooting docs, rules, skills, or when deciding whether content belongs in an existing document or should become a new document.

**触发场景：**

- writing docs
- README files
- runbooks
- architecture notes
- deployment guides
- troubleshooting docs
- rules
- skills

---

## reflect-and-remember

**描述：** |

**触发场景：**

- 相关任务触发

---

## show-dont-tell

**描述：** 信息可视化呈现行为准则。当模型回复中包含对比、步骤、配置、架构等结构化信息时自动激活，确保优先使用表格、代码块、列表、树形结构等可视化格式，而不是纯文字堆砌。触发词：「用表格」「画个图」「列个表」「结构化一下」「别光用文字」「可视化」「对比一下」。即使没有触发词，只要回复中包含适合可视化的结构化信息，本 skill 的规则就应生效。也适用于：「太多字了看不下去」「能不能更直观一点」「整理成表格」等场景。

**触发场景：**

- 相关任务触发

---

## sync-global-rules

**描述：** >

**触发场景：**

- 相关任务触发

---

## sync-skill-to-jay

**描述：** Post-action workflow that triggers automatically after creating a new skill or updating an existing skill. Ask the user whether to sync the skill to the jay-skills repository and publish to remote. Use whenever a SKILL.md has just been created or modified.

**触发场景：**

- 相关任务触发

---

## update-claude-code

**描述：** 更新 Claude Code CLI 到最新版本。当用户说"更新 Claude Code"、"升级 Claude Code"、"update claude code"、"claude code 太旧了"、"执行 install.sh 更新"，或者想让 Claude 自我更新时，立即使用此 skill。不要等用户明确说"用 npm"——只要涉及更新 Claude Code 本身，就使用这个 skill。

**触发场景：**

- 相关任务触发

---

## web-content-fetcher

**描述：** >

**触发场景：**

- 相关任务触发

---
