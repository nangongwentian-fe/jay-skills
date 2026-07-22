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
| [emilkowalski-skills](./plugins/emilkowalski-skills/) | [emilkowalski/skills](https://github.com/emilkowalski/skills) | 动画审查、动画改进、动效机会识别和设计工程准则 |

```bash
codex plugin marketplace add nangongwentian-fe/jay-skills --ref main
codex plugin add taste-skill@jay-skills
codex plugin add code-honor-skill@jay-skills
codex plugin add andrej-karpathy-skills@jay-skills
codex plugin add emilkowalski-skills@jay-skills
```

四个外部插件每周检查一次上游更新，发现变化后分别创建 PR。手动检查、同步和验证命令见 [`docs/upstream-sync.md`](./docs/upstream-sync.md)。

## Skills 列表

| Skill | 描述 |
|-------|------|
| [buddy-reroll](#buddy-reroll) | 重新掷骰 Claude Code 伙伴，获取指定物种、稀有度或闪光变体 |
| [clean-wechat-wps-storage](#clean-wechat-wps-storage) | 清理 macOS 微信和 WPS 本机占用，先扫描、确认计划，再移到废纸篓 |
| [codex-imagegen](#codex-imagegen) | 通过 Codex CLI 的 image_gen 工具在 Claude Code 中生成 AI 图片 |
| [daily-work-summary](#daily-work-summary) | 按指定项目和日期从 Git 提交记录生成中文工作内容总结 |
| [figma-use](#figma-use) | Figma Plugin API 操作的前置必读 skill，必须在调用 use_figma 前加载 |
| [git-topic-commit-push](#git-topic-commit-push) | 按主题拆分 Git 改动，默认使用中文 commit message 创建一个或多个 commit 并推送当前分支 |
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

## clean-wechat-wps-storage

**描述：** 清理 macOS 上微信和 WPS Office 的本机磁盘占用。流程固定为先扫描占用、采访用户清理范围、给出清理计划，用户确认后再把应用数据移动到废纸篓。

**触发场景：**

- 用户说微信、WeChat、Weixin、WPS 或 WPS Office 占用空间太大
- 用户想清理微信聊天记录、聊天图片、视频、表情、附件或缓存
- 用户想清理 WPS 云文档本地缓存、插件、字体、日志或临时文件
- 用户要求清理前先确认范围、给出计划，再执行移动到废纸篓

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

## git-topic-commit-push

**描述：** Create one or more Git commits grouped by coherent change topic, then push the current branch. Use when the user asks to commit and push, submit by topic, split current changes into topical commits, or do "按照主题提交 commit 并 push"; especially when a worktree has mixed staged, unstaged, or untracked changes that need honest commit boundaries before `git push`. Commit messages must be written in Chinese unless the user explicitly requests another language.

**触发场景：**

- 用户要求 commit 并 push
- 用户要求按照主题提交、分主题提交或拆分当前改动
- 工作区同时存在 staged、unstaged 或 untracked 改动，需要先判断 commit 边界
- 需要创建一个或多个诚实概括改动范围的 commit 后推送当前分支

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

**描述：** 信息可视化呈现行为准则。让 GPT 在回复中优先使用表格、代码块、编号列表、树形结构等格式呈现结构化信息，而不是纯文字堆砌。

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
