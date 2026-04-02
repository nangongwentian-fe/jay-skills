# Jay Skills

> Jay 的 AI Agent Skills 集合，适用于 Claude Code / Codex 等 AI 编程工具。

## 安装

```bash
npx skills add https://github.com/nangongwentian-fe/jay-skills -g -y -a claude-code codex
```

安装单个 skill：

```bash
npx skills add https://github.com/nangongwentian-fe/jay-skills --skill <skill-name> -g -y -a claude-code codex
```

---

## Skills 列表

| Skill | 描述 |
|-------|------|
| [buddy-reroll](#buddy-reroll) | 重新摇你的 Claude Code 伴侣，获取指定物种、稀有度或闪光款 |
| [code-review-uncommitted](#code-review-uncommitted) | 对 git 未提交变更进行多维度 code review，含置信度过滤 |
| [exa-unified-research](#exa-unified-research) | 优先使用 Exa 语义搜索替代内置 WebSearch，获取更高质量网络信息 |
| [git-rebase-workflow](#git-rebase-workflow) | 将功能分支 rebase 到最新目标分支，保持提交历史整洁 |
| [lark-beautiful-docs](#lark-beautiful-docs) | 用 callout / grid / 增强表格等富文本格式美化飞书文档 |
| [lark-cli-router](#lark-cli-router) | 飞书 CLI 路由决策：判断用官方 larksuite/cli 还是社区 feishu-cli |
| [persistent-memory](#persistent-memory) | 跨会话记忆协议，让 Claude Code / Cursor / Codex 等工具共享记忆 |
| [reflect-and-remember](#reflect-and-remember) | 任务完成后自动反思，将值得复用的知识写入持久记忆 |
| [sync-global-rules](#sync-global-rules) | 同步 Awesome-GlobalRule 仓库到本地 Claude Code / Codex 配置 |
| [sync-skill-to-jay](#sync-skill-to-jay) | 新增或更新 skill 后，将其同步到 jay-skills 并发布到远程 |
| [update-claude-code](#update-claude-code) | 一键更新 Claude Code CLI 到最新版本 |
| [web-content-fetcher](#web-content-fetcher) | 渐进回退策略抓取任意网页内容，支持付费墙绕过、Markdown 提取 |

---

## buddy-reroll

**描述：** 重新摇你的 Claude Code 伴侣（companion），获取指定物种、稀有度或闪光款。

**触发场景：**
- 用户说「reroll buddy」「change my buddy」「I want a shiny buddy」
- 用户说「give me a legendary dragon」或 `/buddy-reroll`
- 任何想自定义 Claude Code 伴侣宠物的请求

**原理：** Buddy 生成是确定性的：`hash(userId + SALT)` 决定物种、稀有度、闪光等属性。通过暴力枚举 SALT 最多 500k 次，找到满足条件的结果。

**可选属性：**
- **物种（18 种）**：duck, goose, blob, cat, dragon, octopus, owl, penguin, turtle, snail, ghost, axolotl, capybara, cactus, robot, rabbit, mushroom, chonk
- **稀有度**：common (60%)、uncommon (25%)、rare (10%)、epic (4%)、legendary (1%)

---

## code-review-uncommitted

**描述：** 对 git 中未提交的代码变更进行多维度 code review。

**触发场景：**
- 用户要求「review 未提交的代码」「review 当前改动」
- 使用 `/code-review-uncommitted`

**审查维度：**
- 项目规范合规性
- Bug 扫描
- 代码注释合规性
- 组件封装 / 架构设计合理性
- 置信度评分过滤误报（低置信度问题不上报）

---

## exa-unified-research

**描述：** 优先使用 Exa 语义搜索替代内置 WebSearch/WebFetch，获取更高质量的网络信息。

**触发场景：**
- 搜索网页、查找人物 / 公司信息
- 寻找代码示例或 API 用法
- 阅读技术博客、学术论文、X/Twitter 内容
- 任何需要当前在线信息的任务

**优势：** Exa 使用神经语义搜索，针对 AI pipeline 优化，比关键词搜索返回更高质量的结果。在回退到 WebSearch 之前始终优先调用此 skill。

---

## git-rebase-workflow

**描述：** 将当前功能分支 rebase 到最新的目标分支（如 master/main），保持提交历史整洁。

**触发场景：**
- 功能分支落后于目标分支，需要同步最新代码
- 想避免 merge commit，保持线性历史

---

## lark-beautiful-docs

**描述：** 让飞书文档不朴素，强制使用富文本格式，杜绝纯文字堆砌。

**触发场景：**
- 用户要求写飞书文档、整理文档、美化文档
- 输出任何飞书 / Lark 文档内容时

**支持格式：**
- 高亮块（callout）
- 分栏（grid）
- 增强表格（lark-table）
- 画板、图表

与 `lark-doc` skill 配合使用：lark-doc 负责执行写入命令，本 skill 负责排版设计决策。

---

## lark-cli-router

**描述：** 操作飞书 CLI 时的路由决策 skill，判断该用官方 larksuite/cli 还是社区 feishu-cli。

**触发场景：**
- 需要操作飞书 / Lark CLI
- 飞书文档导入导出、Markdown 与飞书文档互转
- Mermaid / PlantUML 导入
- 通用 Lark / 飞书平台 API 操作
- 本机未安装对应 CLI 时，自动检查并按 README 推荐方式安装

---

## persistent-memory

**描述：** 通用跨会话记忆协议（Universal Memory Protocol），让所有 AI 编程工具共享同一套记忆系统。

**触发场景：**
- 用户说「记住」
- 用户问「之前」某事
- 检测到敏感信息
- 会话结束时

**支持工具：** Claude Code / Cursor / Aider / Cline / Codex / Trae / OpenCode

**能力：** 智能分类 / FSRS 衰减 / 月度压缩 / 多层检索

---

## reflect-and-remember

**描述：** 任务完成后的反思记忆 skill，主动将值得跨会话复用的知识写入持久记忆。

**触发场景：**
- 完成部署、调试、架构决策等重要任务后
- 踩坑或发现反直觉行为后
- 发现项目特有的规律 / 约定后
- 用户说「记住」「记录」「别忘了」「remember」时

**不触发：** 简单代码修改、格式调整等轻量任务。

**写入规则：** 团队共享知识写入项目 `.claude/memory/`（进 git），敏感信息写入用户私有 memory（不进 git）。

---

## sync-global-rules

**描述：** 同步 `nangongwentian-fe/Awesome-GlobalRule` 仓库到本地 AI 编程工具配置。

**触发场景：**
- 用户说「同步规则」「同步 global rule」「检查规则更新」
- 「更新 agent rules」「sync global rules」「规则有没有更新」「拉取最新规则」

**同步目标：** Claude Code (`~/.claude/`) 和 Codex (`~/.codex/`)

**功能：** 自动备份、更新检测、状态追踪

---

## sync-skill-to-jay

**描述：** 新增或更新 skill 后，将其同步到 jay-skills 仓库并发布到远程。

**触发场景：**
- 刚创建或修改了一个 SKILL.md
- 需要把本地 skill 发布到 jay-skills 公共仓库

**工作流：**
1. 定位或克隆 jay-skills 仓库
2. 同步 skill 文件
3. 更新 jay-skills README（自动扫描所有 skill，重新生成介绍文档）
4. Commit & push
5. 删除本地手动副本，通过 npx 重新安装（确保由 skills 框架管理）

---

## update-claude-code

**描述：** 一键更新 Claude Code CLI 到最新版本。

**触发场景：**
- 用户说「更新 Claude Code」「升级 Claude Code」「update claude code」
- 「claude code 太旧了」「执行 install.sh 更新」
- 任何涉及更新 Claude Code 本身的请求

---

## web-content-fetcher

**描述：** 网页内容获取技巧集合，渐进回退策略确保拿到内容。

**触发场景：**
- 抓取网页内容、提取文章正文
- 读取任意 URL 的文本或 Markdown 格式内容
- 访问 X/Twitter、微信、知乎、Medium 等平台内容
- 绕过付费墙

**回退策略：**
1. WebFetch 直接抓取（最快，先试）
2. 如失败，并行尝试 `r.jina.ai` 和 `defuddle.md` 代理，取内容更完整的结果
3. 如代理也失败，使用 WebSearch 兜底
