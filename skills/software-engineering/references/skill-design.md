# 设计依据与取舍

调研日期：2026-11-15。以下用于维护，不要求每次开发联网重读。正文为针对用户工作方式的重新组织，不复制外部技能全文或引入其运行脚本。

| 来源 | 借鉴 | 未采用 |
| --- | --- | --- |
| [Agent Skills 官方最佳实践](https://agentskills.io/skill-creation/best-practices) | 来自真实纠错的规则、清晰触发、渐进披露、执行反馈 | 通用口号或软件工程百科 |
| [Anthropic skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) | 任务用例、独立执行、基线比较与迭代 | 强化触发到无关任务、Claude 专属评测 CLI、自动启动评测网页 |
| [Vercel React best practices](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/SKILL.md) | 按问题类别路由与风险优先级 | 无条件套用 Next.js 规则、未经测量的优化 |
| [Superpowers systematic-debugging](https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md) | 先找失败边界、证据驱动假设、修复后验证 | 每个小改动固定四阶段、所有改动强制新增测试或委派 |
| [Skills 目录](https://skills.sh/) | 发现社区使用的候选，再读其原始仓库 | 把安装量、星数当作质量或适配性证据 |

## 本技能的组织

软件开发的共同契约留在入口；前端专项保留原有内容，通过前端路由按需加载。后端与 Agent 参考只补会改变实现或验证决策的边界，不维护框架 API 手册。独立 Git、浏览器、部署与框架技能继续由各自入口负责，避免多份规则漂移。

2026-11-21 将原 reuse-first 技能并入为 [复用优先](reuse-first.md)：用户只在写代码时使用它，单独触发反而可能在编码任务中漏加载。非代码场景（模板、表格流程等）随之不再覆盖。commit-before-deploy 保持独立：部署的触发词、外部副作用和停止条件与日常编码不同，并入会让每次编码都加载发布规则。

"项目服务由用户启动"同时写入用户的全局指令（~/.codex/AGENTS.md、~/.claude/CLAUDE.md），使它在本技能未触发时也生效；本技能保留精简版，修改时两处同步。

“项目未启动时告知用户，由用户启动”来自用户明确的跨项目工作偏好。一次“终止你启动的”不是永久停服指令，因此保留的是进程归属与授权原则，不将那次清理动作固化为每次工作步骤。一次性检查不等于项目服务；是否隐式拉起服务须检查脚本。

技能入口从 frontend-engineering 迁移为 software-engineering；不保留两个自动发现的重复正文。旧版完整基线放在技能发现目录之外，作为回滚与评测依据。其他项目若显式引用旧名字或路径，应在其授权范围内更新，不能静默批量修改无关仓库。

## 维护与验证

新增规则需有实际失败或明确任务依据，写清触发条件、动作与退出条件；仅涉及某领域的知识放专项。行为变更用独立上下文执行受影响任务及关键回归。显式加载的测试不能证明自然触发；结构校验不能证明行为。

前端原有依据见 [sources.md](sources.md)。专项参考是实现时的检查线索，不承诺真实数据库、模型或浏览器已经验收。

后端授权边界可按 [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)核查请求级与对象级授权；Agent 状态语义参考 [LangGraph Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)。这些是专项核对入口，不能用文档中的能力介绍推断当前项目已经配置或验收。

图片资产规则来自生成背景接入后的用户纠错：仅把 PNG 转 JPEG，遗漏尺寸优化与现代格式评估。规则限定于图片接入和优化，保留矢量、透明、动画与兼容性边界，不固化某次像素尺寸或质量参数。
