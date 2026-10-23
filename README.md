# Jay Skills

> Jay 的 AI Agent 资源集合，包含可安装的 Skills 和可执行的 Playbooks，适用于 Claude Code / Codex 等 AI 编程工具。

## 内容模块

| 模块 | 目录 | 用途 |
|------|------|------|
| Skills | [`skills/`](./skills/) | 可通过 `npx skills add` 安装，由 Agent 按场景触发 |
| Codex Plugin | [`.codex-plugin/`](./.codex-plugin/) | 通过 Codex Marketplace 安装，直接加载本仓全部 Skills |
| Playbooks | [`playbooks/`](./playbooks/) | 给 Agent 读取并按步骤执行的专题教程，不是可安装 skill |

## Skills CLI 安装

以下命令只安装 `skills/` 下的内容，不会安装 `playbooks/`。

```bash
# 安装全部 skills
npx skills add nangongwentian-fe/jay-skills --global

# 安装单个 skill
npx skills add nangongwentian-fe/jay-skills --skill <skill-name> --global
```

## Codex 插件

Codex 插件直接加载本仓 `skills/`，不复制 Skill 文件，也不会将 `playbooks/` 作为 Skill 加载。

### 安装

```bash
codex plugin marketplace add nangongwentian-fe/jay-skills --ref main
codex plugin add jay-skills@jay-skills
```

### 发布 Skill 更新

修改或新增 Skill 后，提交前刷新插件版本：

```bash
python3 scripts/update_codex_plugin_version.py
```

该命令保留基础版本，并将现有 build metadata 替换为 UTC cachebuster。请将 Skill 改动与 `.codex-plugin/plugin.json` 一起提交。`sync-skill-to-jay` 仍可用于 Skills CLI 的发布与全局安装，但不是 Codex 插件更新的必需步骤。

### 获取更新

Codex App 显示新版本后可直接点击更新。CLI 可使用以下回退流程：

```bash
codex plugin marketplace upgrade jay-skills
codex plugin add jay-skills@jay-skills
```

更新完成后，请新建 Codex 任务以加载新版 Skills。

## Skills 列表

| Skill | 描述 |
|-------|------|
| [buddy-reroll](#buddy-reroll) | 按明确要求定制 Claude Code 伙伴，保留选择与应用边界。 |
| [clean-wechat-wps-storage](#clean-wechat-wps-storage) | 扫描 macOS 微信和 WPS 占用，确认具体清理计划后将选定内容移到废纸篓。 |
| [codex-imagegen](#codex-imagegen) | 宿主缺少原生图像工具时，通过 Codex CLI 生成或编辑位图，并验证本次调用返回的资产。 |
| [daily-work-summary](#daily-work-summary) | 按指定仓库和日期，仅依据本人 Git 提交生成中文日报。 |
| [find-docs](#find-docs) | 通过 Context7 核对当前库、API 与 CLI 契约 |
| [git-topic-commit-push](#git-topic-commit-push) | 按授权范围精确组织主题提交，仅在已授权时推送；保护既有暂存内容。 |
| [maintainable-frontend-styles](#maintainable-frontend-styles) | 沿用项目样式体系实现或重构局部样式，按受影响行为选择参考与验证。 |
| [progressive-disclosure-docs](#progressive-disclosure-docs) | 按主题和读者意图组织文档，将细节放到按需引用的所属文档。 |
| [post-implementation-review-gate](#post-implementation-review-gate) | 对存在实质兼容性、安全或行为风险的实现执行独立评审、证据核验与范围内修复。 |
| [post-task-learning-review](#post-task-learning-review) | 有可复用发现时维护任务范围内文档或技能；记忆写入遵循当前权威协议。 |
| [shenzhen-social-insurance](#shenzhen-social-insurance) | 查询深圳医保、养老与失业待遇，核实逐月缴费并指导灵活就业续保。 |
| [show-dont-tell](#show-dont-tell) | 用合适的表格、列表或图示帮助理解复杂信息，简单回复保持简洁。 |
| [split-ui-components](#split-ui-components) | 按业务职责与状态归属拆分或评审 UI 组件，保持外部契约并针对性验证。 |
| [sync-skill-to-jay](#sync-skill-to-jay) | 以仓库为源码入口完成已授权的发布与安装，区分本地版本和已验证远端版本。 |
| [web-content-fetcher](#web-content-fetcher) | 使用可用工具获取公开网页正文，按实际缺失渐进回退，不绕过登录或付费墙。 |
| [yeungnam-notices](#yeungnam-notices) | 查询韩国岭南大学计算机学部公告，核对考试安排与附件修订。 |

## Playbooks 列表

| Playbook | 描述 |
|----------|------|
| [agent-development-standards](./playbooks/agent-development-standards/) | 按任务路由开发规范、校验命令与技能决策场景 |
| [codex-clash-proxy](./playbooks/codex-clash-proxy/) | 让 macOS/Windows 的 Codex CLI 或 Codex.app 单独走本地代理，包含 Clash 与 Windows 365VPN 启动器 |

---

## buddy-reroll

按明确要求定制 Claude Code 伙伴，保留选择与应用边界。

适用条件与操作约束见 [SKILL.md](./skills/buddy-reroll/SKILL.md)。

---

## clean-wechat-wps-storage

扫描 macOS 微信和 WPS 占用，确认具体清理计划后将选定内容移到废纸篓。

适用条件与操作约束见 [SKILL.md](./skills/clean-wechat-wps-storage/SKILL.md)。

---

## codex-imagegen

宿主缺少原生图像工具时，通过 Codex CLI 生成或编辑位图，并验证本次调用返回的资产。

适用条件与操作约束见 [SKILL.md](./skills/codex-imagegen/SKILL.md)。

---

## daily-work-summary

按指定仓库和日期，仅依据本人 Git 提交生成中文日报。

适用条件与操作约束见 [SKILL.md](./skills/daily-work-summary/SKILL.md)。

---

## find-docs

按具体文档问题查询当前库、API 或 CLI 契约，命令流程见 [SKILL.md](./skills/find-docs/SKILL.md)。

---

## git-topic-commit-push

按授权范围精确组织主题提交，仅在已授权时推送；保护既有暂存内容。

适用条件与操作约束见 [SKILL.md](./skills/git-topic-commit-push/SKILL.md)。

---

## maintainable-frontend-styles

沿用项目样式体系实现或重构局部样式，按受影响行为选择参考与验证。

适用条件与操作约束见 [SKILL.md](./skills/maintainable-frontend-styles/SKILL.md)。

---

## progressive-disclosure-docs

按主题和读者意图组织文档，将细节放到按需引用的所属文档。

适用条件与操作约束见 [SKILL.md](./skills/progressive-disclosure-docs/SKILL.md)。

---

## post-implementation-review-gate

对存在实质兼容性、安全或行为风险的实现执行独立评审、证据核验与范围内修复。

适用条件与操作约束见 [SKILL.md](./skills/post-implementation-review-gate/SKILL.md)。

---

## post-task-learning-review

有可复用发现时维护任务范围内文档或技能；记忆写入遵循当前权威协议。

适用条件与操作约束见 [SKILL.md](./skills/post-task-learning-review/SKILL.md)。

---

## shenzhen-social-insurance

查询深圳医保、养老与失业待遇，区分待遇月份和实际缴费入账，并依据当前官方页面指导灵活就业续保。

适用条件与操作边界见 [SKILL.md](./skills/shenzhen-social-insurance/SKILL.md)。

---

## show-dont-tell

用合适的表格、列表或图示帮助理解复杂信息，简单回复保持简洁。

适用条件与操作约束见 [SKILL.md](./skills/show-dont-tell/SKILL.md)。

---

## split-ui-components

按业务职责与状态归属拆分或评审 UI 组件，保持外部契约并针对性验证。

适用条件与操作约束见 [SKILL.md](./skills/split-ui-components/SKILL.md)。

---

## sync-skill-to-jay

以仓库为源码入口完成已授权的发布与安装，区分本地版本和已验证远端版本。

适用条件与操作约束见 [SKILL.md](./skills/sync-skill-to-jay/SKILL.md)。

---

## web-content-fetcher

使用可用工具获取公开网页正文，按实际缺失渐进回退，不绕过登录或付费墙。

适用条件与操作约束见 [SKILL.md](./skills/web-content-fetcher/SKILL.md)。

---

## yeungnam-notices

查询韩国岭南大学计算机学部公告，按课程编号核对考试时间表、附件修订和来源冲突。

适用条件与操作约束见 [SKILL.md](./skills/yeungnam-notices/SKILL.md)。
