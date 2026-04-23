# de-gpt-ify 安装指南

本文件面向 AI Agent（Claude Code / Codex），说明如何完成 de-gpt-ify skill 的完整安装。

## 安装步骤

### 1. 安装 skill 文件

```bash
npx skills add https://github.com/nangongwentian-fe/jay-skills --skill de-gpt-ify -g -y -a claude-code codex
```

### 2. 执行 install.sh（关键步骤，不可跳过）

安装 skill 文件后，必须运行安装脚本将核心风格规则写入 `~/.codex/AGENTS.md`：

```bash
~/.agents/skills/de-gpt-ify/scripts/install.sh
```

这一步的作用：将精简版中文风格规则追加到 `~/.codex/AGENTS.md`，使 Codex 中的 GPT 模型在每次对话中都自动遵守规则。

如果跳过这一步，规则只在 skill 被显式触发时才生效，无法覆盖日常对话。

### 3. 验证

运行以下命令确认规则已写入：

```bash
grep "de-gpt-ify" ~/.codex/AGENTS.md
```

预期输出应包含 `<!-- de-gpt-ify:start -->` 标记。

## 卸载

```bash
~/.agents/skills/de-gpt-ify/scripts/install.sh --uninstall
```

这会从 `~/.codex/AGENTS.md` 中移除 de-gpt-ify 规则块，不影响其他内容。

## 工作原理

本 skill 采用两层架构：

| 层 | 文件 | 加载方式 | 作用 |
|---|---|---|---|
| 第 1 层 | `~/.codex/AGENTS.md` 中的规则块 | 每次对话始终加载 | 核心风格约束，解决 80% 黑话问题 |
| 第 2 层 | `SKILL.md` 完整内容 | 用户说"去黑话""讲人话"等时按需加载 | 深度清洗、黑话检测报告、详细词表 |

`install.sh` 负责第 1 层的写入。写入内容带有 `<!-- de-gpt-ify:start/end -->` 标记，支持幂等操作和干净卸载。
