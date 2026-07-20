# Jay Skills

> Jay 的 AI Agent 资源集合，包含可安装的 Skills 和可执行的 Playbooks，适用于 Claude Code / Codex 等 AI 编程工具。

## 内容模块

| 模块 | 目录 | 用途 |
|------|------|------|
| Skills | [`skills/`](./skills/) | 可通过 `npx skills add` 安装，由 Agent 按场景触发 |
| Plugins | [`plugins/`](./plugins/) | 可通过 Codex 插件市场安装，打包一组相关 skills |
| Playbooks | [`playbooks/`](./playbooks/) | 给 Agent 读取并按步骤执行的专题教程，不是可安装 skill |

## 安装

以下命令只安装 `skills/` 下的内容，不会安装 `playbooks/`。

```bash
# 安装全部 skills
npx skills add https://github.com/nangongwentian-fe/jay-skills -g -y -a claude-code codex

# 安装单个 skill
npx skills add https://github.com/nangongwentian-fe/jay-skills --skill <skill-name> -g -y -a claude-code codex
```

## Codex 插件

| Plugin | 来源 | 内容 |
|--------|------|------|
| [taste-skill](./plugins/taste-skill/) | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | 前端设计、改版、image-to-code、视觉风格和图片生成 skills |
| [code-honor-skill](./plugins/code-honor-skill/) | [xxxily/code-honor-skill](https://github.com/xxxily/code-honor-skill) | 程序员八荣八耻编码准则、Code Review 模板和代码扫描工具 |
| [andrej-karpathy-skills](./plugins/andrej-karpathy-skills/) | [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | 思考优先、保持简单、精准修改和目标驱动验证的编码准则 |

```bash
codex plugin marketplace add nangongwentian-fe/jay-skills --ref main
codex plugin add taste-skill@jay-skills
codex plugin add code-honor-skill@jay-skills
codex plugin add andrej-karpathy-skills@jay-skills
```

三个外部插件每周检查一次上游更新，发现变化后分别创建 PR。手动检查、同步和验证命令见 [`docs/upstream-sync.md`](./docs/upstream-sync.md)。

## Skills 列表

| Skill | 描述 |
|-------|------|
| [buddy-reroll](#buddy-reroll) | 重新掷骰 Claude Code 伙伴，获取指定物种、稀有度或闪光变体 |
| [browser-mcp-resource-guard](#browser-mcp-resource-guard) | 控制浏览器自动化 MCP 的 CPU、内存、能耗和清理风险 |
| [clean-wechat-wps-storage](#clean-wechat-wps-storage) | 清理 macOS 微信和 WPS 本机占用，先扫描、确认计划，再移到废纸篓 |
| [code-review-uncommitted](#code-review-uncommitted) | 对 git 未提交变更进行多维度 code review，含规范合规性、Bug 扫描、置信度过滤 |
| [codex-imagegen](#codex-imagegen) | 通过 Codex CLI 的 image_gen 工具在 Claude Code 中生成 AI 图片 |
| [daily-work-summary](#daily-work-summary) | 按指定项目和日期从 Git 提交记录生成中文工作内容总结 |
| [de-gpt-ify](#de-gpt-ify) | 中文输出去黑话化，让 GPT 像人一样说中文，告别咨询黑话和 AI 味表达 |
| [exa-unified-research](#exa-unified-research) | 偏好网络研究工具，使用 Exa 神经语义搜索替代内置 WebSearch/WebFetch |
| [figma-use](#figma-use) | Figma Plugin API 操作的前置必读 skill，必须在调用 use_figma 前加载 |
| [git-commit](#git-commit) | 基于当前 git 工作区变更生成并创建单个提交 |
| [git-rebase-workflow](#git-rebase-workflow) | Git Rebase 分支同步流程，保持提交历史整洁 |
| [git-topic-commit-push](#git-topic-commit-push) | 按主题拆分 Git 改动，默认使用中文 commit message 创建一个或多个 commit 并推送当前分支 |
| [goal-loop-builder](#goal-loop-builder) | 生成文件引用式 `/goal` prompt、可验证 `goal.md` 和 `/loop` 运行契约 |
| [ikuncode-image-gen](#ikuncode-image-gen) | 使用 IKunCode Gemini 图像预览模型生成或编辑图片 |
| [llm-wiki](#llm-wiki) | 查询和操作本地 LLM Wiki，支持 API、MCP 与固定项目文件回退 |
| [progressive-disclosure-docs](#progressive-disclosure-docs) | 用渐进式披露设计、拆分和维护文档，避免 README 或单个文档无限膨胀 |
| [post-task-learning-review](#post-task-learning-review) | 任务完成后直接维护经验，自动新增、更新、合并或删除项目文档、memory 或 skill |
| [search-jay-llm-wiki](#search-jay-llm-wiki) | 在相关非平凡任务前主动检索 jay-llm-wiki 中的既有研究与工程经验 |
| [show-dont-tell](#show-dont-tell) | 信息可视化呈现，让 GPT 优先用表格、代码块、列表呈现结构化信息 |
| [sync-skill-to-jay](#sync-skill-to-jay) | 创建或更新 skill 后，询问是否同步到 jay-skills 仓库并发布 |
| [update-claude-code](#update-claude-code) | 更新 Claude Code CLI 到最新版本 |
| [web-content-fetcher](#web-content-fetcher) | 网页内容获取技巧集合，覆盖 Markdown 提取、付费墙绕过等场景 |

## Playbooks 列表

| Playbook | 描述 |
|----------|------|
| [codex-clash-proxy](./playbooks/codex-clash-proxy/) | 让 macOS/Windows 的 Codex CLI 或 Codex.app 单独走本地代理，包含 Clash 与 Windows 365VPN 启动器 |

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

## browser-mcp-resource-guard

**描述：** 控制浏览器自动化 MCP 工具带来的 CPU、内存、电池、风扇和重复进程风险，覆盖 Chrome DevTools MCP、Playwright MCP、`@playwright/mcp` 及相关 Chrome Helper 进程。

**触发场景：**

- 准备使用、正在使用或刚用完 Chrome DevTools MCP、Playwright MCP、`@playwright/mcp` 等浏览器自动化 MCP
- 用户提到高 CPU、高能耗、电池消耗、风扇、发热、卡顿
- 用户提到重复浏览器 MCP 进程、残留 Chrome Helper、MCP 清理
- 长时间 Codex 会话可能留下浏览器自动化 MCP 辅助进程

---

## clean-wechat-wps-storage

**描述：** 清理 macOS 上微信和 WPS Office 的本机磁盘占用。流程固定为先扫描占用、采访用户清理范围、给出清理计划，用户确认后再把应用数据移动到废纸篓。

**触发场景：**

- 用户说微信、WeChat、Weixin、WPS 或 WPS Office 占用空间太大
- 用户想清理微信聊天记录、聊天图片、视频、表情、附件或缓存
- 用户想清理 WPS 云文档本地缓存、插件、字体、日志或临时文件
- 用户要求清理前先确认范围、给出计划，再执行移动到废纸篓

---

## code-review-uncommitted

**描述：** 对 git 中未提交的代码变更进行多维度 code review，包括项目规范合规性、Bug 扫描、代码注释合规性、组件封装/架构设计合理性审查，并通过置信度评分过滤误报。当用户要求 review 未提交的代码、review 当前改动、或使用 /code-review-uncommitted 时触发。

**触发场景：**

- 要求 review 未提交的代码
- 要求 review 当前改动 / diff
- 使用 `/code-review-uncommitted`

---

## codex-imagegen

**描述：** 通过 Codex CLI 的内置 `image_gen.imagegen` 工具（gpt-image-2）在 Claude Code 中生成 AI 图片。Claude Code 本身没有图片生成能力，这个 skill 利用 `codex exec` 非交互模式桥接 Codex 的图片生成工具，无需单独配置 `OPENAI_API_KEY`。

**触发场景：**

- 用户说"生成图片""画一张图""做个海报""生成一张照片""帮我画""生成插画"
- 用户说 "generate an image" "create a photo of" "make an illustration" "design a poster"
- 需要生成写实照片、插画、概念图、产品图、游戏素材、UI 模型图等 AI 位图
- 需要透明背景图片（通过 chroma-key 去背景流程）

**效果示例：**

- "帮我生成一张暖色调的咖啡店内部照片" → 通过 Codex 生成写实风格咖啡店图片
- "Generate a pixel art sword icon, transparent background" → 生成像素剑 + chroma-key 去绿幕
- "给项目生成一张 hero image，蓝紫科技感" → 生成 AI 主题 landing page 配图并保存到指定路径

---

## daily-work-summary

**描述：** 根据指定 Git 仓库和日期，从 commit、提交正文、文件变更及必要的 diff 中提炼每日工作内容。用于用户要求按项目和日期生成日报、每日工作总结、根据 Git commit 总结工作，或要求用 1、2、3 编号列出某天或某段日期完成事项的场景。

**触发场景：**

- 按指定项目和日期生成日报或每日工作总结
- 根据 Git commit 汇总单日、多个日期或日期区间的完成事项
- 用简洁的中文编号清单列出工作内容

**效果示例：**

- `总结 E:\Code\Project\Demo 2026-07-16 的工作内容。` → 输出当天的编号工作事项
- `总结当前项目 7 月 16 日和 7 月 17 日的工作内容。` → 按日期分组并分别编号
- `总结 D:\work\app 2026-07-01 至 2026-07-05 的每日工作。` → 覆盖区间内每个日期
- 指定日期没有提交 → 输出“该日期没有已提交工作内容。”

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

## git-topic-commit-push

**描述：** Create one or more Git commits grouped by coherent change topic, then push the current branch. Use when the user asks to commit and push, submit by topic, split current changes into topical commits, or do "按照主题提交 commit 并 push"; especially when a worktree has mixed staged, unstaged, or untracked changes that need honest commit boundaries before `git push`. Commit messages must be written in Chinese unless the user explicitly requests another language.

**触发场景：**

- 用户要求 commit 并 push
- 用户要求按照主题提交、分主题提交或拆分当前改动
- 工作区同时存在 staged、unstaged 或 untracked 改动，需要先判断 commit 边界
- 需要创建一个或多个诚实概括改动范围的 commit 后推送当前分支

---

## goal-loop-builder

**描述：** Create copy-ready, verifiable run contracts for long-horizon agent work. Use when the user asks to write, improve, or review Codex `/goal` prompts, Claude Code `/goal` conditions, Claude `/loop` prompts, `.claude/loop.md`, `goal.md`, loop engineering prompts, autonomous run instructions, stop/pause conditions, verification criteria, bounded iteration policy, or persistent Markdown instructions for agents.

**触发场景：**

- 编写、改进或评审 Codex `/goal` prompt
- 编写 Claude Code `/goal` 完成条件或运行契约
- 编写 Claude `/loop` 定时轮询 prompt
- 编写 `.claude/loop.md` 或 `goal.md` 持久化说明
- 为长任务定义验证证据、边界、迭代策略、停止条件和暂停条件

**效果示例：**

User: "帮我做个 App"

Output: Recommend Codex or Claude `/goal`, create a real `app-mvp.goal.md`, then return a short one-line `/goal Read @/absolute/path/app-mvp.goal.md ...` prompt.

User: "让它每 5 分钟检查部署是否完成"

Output: Recommend Claude `/loop 5m ...`, include observation signals, reporting format, stop/escalation conditions, and optional `.claude/loop.md`.

User: "修复现有仓库的 flaky test"

Output: Recommend `/goal`, create a real `flaky-test.goal.md`, then return a short `/goal` prompt that references it and requires discovery of test commands, isolated fix boundaries, regression evidence, and pause on missing repro or environment blockers.

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

## llm-wiki

**描述：** Operate the user's locally running LLM Wiki desktop app and its project files. Use when the user explicitly names LLM Wiki, my wiki, 知识库, a Wiki page/project, graph, review queue, Wiki Agent chat, or source rescan; also use when another skill such as search-jay-llm-wiki requests LLM Wiki retrieval or authorized filesystem maintenance. Covers LLM Wiki 0.6.4 health, projects, file listing/read, reviews, hybrid search, Agent chat and cancellation, graph navigation, source rescan, and the fixed jay-llm-wiki filesystem fallback. Do not trigger for Obsidian, Notion, generic notes, or unrelated knowledge tools.

**触发场景：**

- 用户明确提到 LLM Wiki、知识库、Wiki 页面或项目
- 查询 Review、图谱、Wiki Agent Chat 或重扫来源
- `$search-jay-llm-wiki` 请求任务前知识检索
- 已授权的 Wiki 文件维护

---

## progressive-disclosure-docs

**描述：** 用渐进式披露设计、拆分和维护 Markdown / 项目文档，让读者和 agent 先看到必要信息，需要时再进入细节，避免 README 或单个文档无限膨胀。

**触发场景：**

- 编写或修改 README、部署文档、排障文档、架构说明
- 判断内容应该放进已有文档还是新建专题文档
- 为项目文档、规则文档、skill 文档设计层级和入口
- 发现文档越来越大、主题混杂，需要拆分或重组

---

## post-task-learning-review

**描述：** 任务完成后直接维护长期可复用经验，判断并执行新增、更新、合并、删除或不处理，并在项目文档、Codex memory、已有 skill 或新 skill 之间选择合适位置。

**触发场景：**

- 完成复杂排障、部署、线上验证、文档维护、重复 workflow 发现
- 创建或更新 skill 后，需要判断经验是否应继续进入项目文档、memory 或 skill
- 用户问“这次有什么值得记忆/写进文档/做成 skill”
- 满足维护条件且处于当前权限范围时，直接写入，不再二次请求用户确认

**安装后额外步骤：**

```bash
~/.agents/skills/post-task-learning-review/scripts/install.sh
```

---

## search-jay-llm-wiki

**描述：** Proactively search the fixed jay-llm-wiki before relevant non-trivial research, architecture, technology selection, complex debugging, or complex implementation tasks when prior Deep Research or reusable engineering knowledge may help. Use even when the user does not explicitly mention LLM Wiki. Invoke `$llm-wiki` for transport, cite the Wiki paths used, and verify time-sensitive claims with current first-party sources. Skip translation, formatting, simple calculations, one-line commands, casual conversation, and clearly unrelated self-contained tasks.

**触发场景：**

- 研究、架构设计、技术选型、复杂调试或复杂开发
- 可能复用既有 Deep Research、跨项目结论或工程经验的非平凡任务
- 用户未明确提到 Wiki，但既有知识可能影响任务方法

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
