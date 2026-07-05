# post-task-learning-review 安装指南

本文件面向 AI Agent（Claude Code / Codex），说明如何完成 post-task-learning-review skill 的完整安装。

## 安装步骤

### 1. 安装 skill 文件

```bash
npx skills add https://github.com/nangongwentian-fe/jay-skills --skill post-task-learning-review -g -y -a claude-code codex
```

### 2. 执行 install.sh（关键步骤，不可跳过）

安装 skill 文件后，必须运行安装脚本将任务后经验维护规则写入 `~/.codex/AGENTS.md`：

```bash
~/.agents/skills/post-task-learning-review/scripts/install.sh
```

如果跳过这一步，规则只在 skill 被显式触发时才生效，无法让 agent 在非平凡任务结束后主动复盘经验。

### 3. 验证

```bash
grep "post-task-learning-review" ~/.codex/AGENTS.md
```

预期输出应包含 `<!-- post-task-learning-review:start -->` 标记。

## 卸载

```bash
~/.agents/skills/post-task-learning-review/scripts/install.sh --uninstall
```

## 工作原理

与 show-dont-tell 相同的两层架构：

| 层 | 文件 | 加载方式 | 作用 |
|---|---|---|---|
| 第 1 层 | `~/.codex/AGENTS.md` 中的规则块 | 每次对话始终加载 | 提醒 agent 在非平凡任务后主动做经验维护判断 |
| 第 2 层 | `SKILL.md` 完整内容 | 按需加载 | 判断经验应新增、更新、合并、删除，还是不处理 |

`install.sh` 负责第 1 层的写入。写入内容带有 `<!-- post-task-learning-review:start/end -->` 标记，支持幂等安装和干净卸载。
