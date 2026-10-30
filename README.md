# Jay Skills

个人维护的 AI Agent 技能集合，收录开发、文档整理、信息查询和日常工具的可复用工作流程，可通过 Skills CLI 安装到 Codex、Claude Code 等支持技能的工具中。

每个技能以 `SKILL.md` 为入口，说明何时使用、如何执行，以及需要哪些工具或环境。部分技能还附带脚本、参考资料或评测样例；安装技能不会自动安装这些外部依赖。

## 快速开始

需要 Node.js 和 npm，版本要求见 [Skills CLI 官方文档](https://github.com/vercel-labs/skills#install-a-skill)。

```bash
# 交互选择要安装的技能和目标 Agent（全局安装）
npx skills add nangongwentian-fe/jay-skills -g

# 只安装一个技能，例如 daily-work-summary
npx skills add nangongwentian-fe/jay-skills --skill daily-work-summary -g
```

如果只想在某个项目中使用，在该项目目录运行命令并去掉 `-g`。建议先从实际需要的技能开始，安装前查看对应说明中的工具和环境要求。

```mermaid
flowchart LR
    A[按任务选择技能] --> B[阅读 SKILL.md]
    B --> C[安装到目标 Agent]
    C --> D[描述任务或指定技能名]
    D --> E[Agent 按技能流程执行]
```

安装后，在目标 Agent 中描述需求即可；也可以明确写出技能名，例如：

> 使用 daily-work-summary，汇总当前仓库中我在 2026-10-22 提交的工作，生成中文日报。

技能的实际执行依赖当前 Agent 可用的工具、账户权限和运行环境。平台或服务专用技能的要求见下方说明。

## 技能目录

点击技能名可直接查看完整用法。

### 判断与协作

| 技能 | 适合用来做什么 |
| --- | --- |
| [goal-first](./skills/goal-first/SKILL.md) | 理解真实目标，主动发现更直接有效的解决路径；依据证据改进方案，尊重明确约束与合理取舍。 |

### 开发与代码交付

| 技能 | 适合用来做什么 |
| --- | --- |
| [reuse-before-build](./skills/reuse-before-build/SKILL.md) | 实现前核实项目已有能力和标准方案；存在缺口时联网比较成熟方案，确认选型后实现。 |
| [find-docs](./skills/find-docs/SKILL.md) | 通过 Context7 查官方文档，核对库、API 和 CLI 的语法及版本差异。 |
| [dts-docs](./skills/dts-docs/SKILL.md) | 识别飞渡 DTS 产品与版本，查询 Cloud、Explorer、Engine 或 SDK 官方文档，并核对项目实际接入方式。 |
| [split-ui-components](./skills/split-ui-components/SKILL.md) | 判断 UI 组件是否需要拆分，按业务职责和状态归属调整边界，保持原有行为。 |
| [maintainable-frontend-styles](./skills/maintainable-frontend-styles/SKILL.md) | 沿用项目现有样式方案，整理局部样式、复用规则和复杂交互样式。 |
| [chrome-browser-validation](./skills/chrome-browser-validation/SKILL.md) | 通过官方 @Chrome 插件复用现有 Chrome 会话，先发现运行时并分层诊断连接，再完成网页调试、交互测试和截图验收。 |
| [git-topic-commit-push](./skills/git-topic-commit-push/SKILL.md) | 将改动按主题组织成 Git 提交，保留无关修改，并在获得授权后推送。 |

### 文档与工作整理

| 技能 | 适合用来做什么 |
| --- | --- |
| [daily-work-summary](./skills/daily-work-summary/SKILL.md) | 按仓库和日期，从本人 Git 提交生成中文日报，不混入其他人的工作。 |
| [finish-cleanly](./skills/finish-cleanly/SKILL.md) | 交付前核实最终成果，自动清理本任务已无用途的临时文件和重复副本，保留必要证据与回滚资料。 |

### 学习与教学

| 技能 | 适合用来做什么 |
| --- | --- |
| [guided-learning](./skills/guided-learning/SKILL.md) | 确认学习范围后按讲义顺序逐点讲解、逐题批改，每节核对覆盖，依据独立作答证据判断掌握情况。 |

```bash
npx skills add nangongwentian-fe/jay-skills --skill guided-learning -g
```

使用示例：使用 guided-learning，确认学习范围后按这份讲义的章节和页码顺序学习，中文讲解、韩语出题，每次一道题，每节核对遗漏，掌握后再建议进入下一知识点。

### 网页与信息查询

| 技能 | 适合用来做什么 |
| --- | --- |
| [web-content-fetcher](./skills/web-content-fetcher/SKILL.md) | 提取公开网页或文章正文；读取失败时按原因选择替代方式，并说明缺失内容。 |
| [yeungnam-notices](./skills/yeungnam-notices/SKILL.md) | 查询韩国岭南大学计算机学部公告，按课程编号核对考试安排和附件修订。 |
| [shenzhen-social-insurance](./skills/shenzhen-social-insurance/SKILL.md) | 在深圳社保官方门户核实医保、养老及失业待遇，查询缴费记录和续保要求。需要相关账户登录状态。 |

### 图像与日常工具

| 技能 | 适合用来做什么 |
| --- | --- |
| [codex-imagegen](./skills/codex-imagegen/SKILL.md) | 当前 Agent 缺少原生图像工具时，通过具备图像能力的 Codex CLI 生成、编辑或找回本次调用的图片。 |
| [clean-wechat-wps-storage](./skills/clean-wechat-wps-storage/SKILL.md) | 扫描 macOS 微信和 WPS 的存储占用，确认清理计划后将选定内容移到废纸篓。 |
| [buddy-reroll](./skills/buddy-reroll/SKILL.md) | 定制 Claude Code 的 `/buddy` 伙伴物种、稀有度和闪光属性。依赖其内部实现，使用前查看兼容性与操作步骤。 |

## 更新已安装的技能

```bash
# 检查已安装技能是否有更新
npx skills check

# 更新指定技能
npx skills update daily-work-summary
```

更多安装、更新和移除选项见 [Skills CLI 官方文档](https://github.com/vercel-labs/skills)。

## 仓库结构与维护

```text
skills/
└── <skill-name>/
    ├── SKILL.md       # 技能入口与执行流程
    ├── references/    # 按需阅读的参考资料（可选）
    ├── scripts/       # 辅助脚本（可选）
    ├── agents/        # Agent 展示与配置元数据（可选）
    └── evals/         # 评测样例及相关文件（可选）
```

新增或修改技能时，以 `skills/<skill-name>/` 为源码入口，同步更新上方索引，并检查技能引用的文件和命令。提交前检查本地链接、技能目录覆盖和 `git diff --check`；推送后核对本地提交与远端分支是否一致。安装方法见上方“快速开始”。
