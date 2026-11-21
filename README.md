# Jay Skills

个人维护的 AI Agent 技能集合，收录开发、文档整理、信息查询和日常工具的可复用工作流程，可通过 Skills CLI 安装到 Codex、Claude Code 等支持技能的工具中。

每个技能以 `SKILL.md` 为入口，说明何时使用、如何执行，以及需要哪些工具或环境。部分技能还附带脚本、参考资料或评测样例；安装技能不会自动安装这些外部依赖。

## 快速开始

需要 Node.js 和 npm，版本要求见 [Skills CLI 官方文档](https://github.com/vercel-labs/skills#install-a-skill)。

```bash
# 交互选择要安装的技能和目标 Agent（全局安装）
npx skills add nangongwentian-fe/jay-skills -g

# 只安装一个技能，例如 software-engineering
npx skills add nangongwentian-fe/jay-skills --skill software-engineering -g
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

> 使用 software-engineering，修复订单接口的越权读取问题，保留原响应契约并验证。

技能的实际执行依赖当前 Agent 可用的工具、账户权限和运行环境。平台或服务专用技能的要求见下方说明。

## 技能目录

点击技能名可直接查看完整用法。

### 开发与代码交付

| 技能 | 适合用来做什么 |
| --- | --- |
| [reuse-first](./skills/reuse-first/SKILL.md) | 主动发现并推荐已有实现、成熟工具、依赖或模板，避免默认从零实现；覆盖代码与非代码任务，按实际取舍和已有授权执行。 |
| [skill-eval](./skills/skill-eval/SKILL.md) | 在 Codex 中独立执行技能行为评测、比较基线并按证据评分；检查回归，明确失败与未验证范围，不额外授权外部操作。 |
| [skill-install-compat](./skills/skill-install-compat/SKILL.md) | 安装或更新技能后，检查手动调用声明并补齐 Codex 伴随配置，保留原版内容及已有配置。 |
| [sync-to-jay-skills](./skills/sync-to-jay-skills/SKILL.md) | 新技能完成后询问是否同步到 jay-skills；记住本机仓库路径，获得授权后同步技能、更新 README、提交并推送验证。 |
| [find-docs](./skills/find-docs/SKILL.md) | 通过 Context7 查官方文档，核对库、API 和 CLI 的语法及版本差异。 |
| [dts-docs](./skills/dts-docs/SKILL.md) | 识别飞渡 DTS 产品与版本，查询 Cloud、Explorer、Engine 或 SDK 官方文档，并核对项目实际接入方式。 |
| [software-engineering](./skills/software-engineering/SKILL.md) | 实现、调试、重构与审查前端、后端和 Agent 应用，按需加载专项并验证行为；包含组件库混排的间距失效与图片资产交付案例，要求按显示用途优化尺寸、编码并验证实际接入；项目未启动时由用户启动。 |
| [chrome-browser-validation](./skills/chrome-browser-validation/SKILL.md) | 通过官方 @Chrome 插件复用现有 Chrome 会话，先发现运行时并分层诊断连接，再完成网页调试、交互测试和截图验收。 |
| [git-topic-commit-push](./skills/git-topic-commit-push/SKILL.md) | 每完成一个独立主题并通过检查，立即提交、推送并验证远端；逐主题报告交付状态，推送受阻时明确说明并停止积累提交。 |
| [commit-before-deploy](./skills/commit-before-deploy/SKILL.md) | 部署前验证、按主题提交并推送代码，确认远端提交后再构建发布；失败时停止部署。 |

### 文档与工作整理

| 技能 | 适合用来做什么 |
| --- | --- |
| [git-work-report](./skills/git-work-report/SKILL.md) | 仅手动调用；默认按当前分支和今天筛选本人提交，以代码块内的中文编号输出可复制日报，保留待验证事项。 |
| [finish-cleanly](./skills/finish-cleanly/SKILL.md) | 交付前核实最终成果，自动清理本任务已无用途的临时文件和重复副本，保留必要证据与回滚资料。 |

手动生成可复制日报：`$git-work-report 总结今天我提交的工作`。也可指定日期，例如 `$git-work-report 总结 2026-11-15 我提交的工作`。

### 学习与教学

| 技能 | 适合用来做什么 |
| --- | --- |
| [asksia-course-sync](./skills/asksia-course-sync/SKILL.md) | 手动核对 AskSia 课堂转译，统计缺失记录并按课程补存双语 Markdown。 |

### 网页与信息查询

| 技能 | 适合用来做什么 |
| --- | --- |
| [web-content-fetcher](./skills/web-content-fetcher/SKILL.md) | 提取公开网页或文章正文；读取失败时按原因选择替代方式，并说明缺失内容。 |
| [yeungnam-notices](./skills/yeungnam-notices/SKILL.md) | 查询韩国岭南大学计算机学部公告，按课程编号核对考试安排和附件修订。 |
| [yeungnam-courses](./skills/yeungnam-courses/SKILL.md) | 查询韩国岭南大学 URP 专业课程、教师、课表和学分，完整采集各学期班次并导出 CSV，区分0条与无法查询。 |
| [shenzhen-social-insurance](./skills/shenzhen-social-insurance/SKILL.md) | 在深圳社保官方门户核实医保、养老及失业待遇，查询缴费记录，指导灵活就业续保、个缴缴费基数申报与税务缴费核对。需要相关账户登录状态。 |
| [nhis-korea](./skills/nhis-korea/SKILL.md) | 操作韩国国民健康保险个人官网，核对账单、实缴月份、欠费与期限，办理已授权的自动扣款及Kakao电子账单变更。 |

### 图像与日常工具

| 技能 | 适合用来做什么 |
| --- | --- |
| [yizhen-image-download](./skills/yizhen-image-download/SKILL.md) | 从医真云电子胶片保存网页提供的 DICOM 和完整分辨率 PNG，核对全部检查、序列与切片并合并打包。 |
| [codex-imagegen](./skills/codex-imagegen/SKILL.md) | 当前 Agent 缺少原生图像工具时，通过具备图像能力的 Codex CLI 生成、编辑或找回本次调用的图片。 |
| [buddy-reroll](./skills/buddy-reroll/SKILL.md) | 定制 Claude Code 的 `/buddy` 伙伴物种、稀有度和闪光属性。依赖其内部实现，使用前查看兼容性与操作步骤。 |

## 更新已安装的技能

`software-engineering` 替代 `frontend-engineering`，保留此前整合的 `react-engineering`、`split-ui-components` 和 `maintainable-frontend-styles` 能力，并扩展后端与 Agent 工程。迁移时先核对旧安装中的本地定制，安装新技能后移除被替代的旧入口；`chrome-browser-validation` 继续独立维护，供 UI 审查按需使用。

```bash
# 检查已安装技能是否有更新
npx skills check

# 更新指定技能
npx skills update software-engineering
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
