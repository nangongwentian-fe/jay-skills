# show-dont-tell 安装指南

本文件面向 AI Agent（Claude Code / Codex），说明如何完成 show-dont-tell skill 的完整安装。

## 安装步骤

### 1. 安装 skill 文件

```bash
npx skills add https://github.com/nangongwentian-fe/jay-skills --skill show-dont-tell -g -y -a claude-code codex
```

### 2. 执行 install.sh（关键步骤，不可跳过）

安装 skill 文件后，必须运行安装脚本将核心可视化规则写入 `~/.codex/AGENTS.md`：

```bash
~/.agents/skills/show-dont-tell/scripts/install.sh
```

如果跳过这一步，规则只在 skill 被显式触发时才生效，无法覆盖日常对话。

### 3. 验证

```bash
grep "show-dont-tell" ~/.codex/AGENTS.md
```

预期输出应包含 `<!-- show-dont-tell:start -->` 标记。

## 卸载

```bash
~/.agents/skills/show-dont-tell/scripts/install.sh --uninstall
```

## 工作原理

与 de-gpt-ify 相同的两层架构：

| 层 | 文件 | 加载方式 | 作用 |
|---|---|---|---|
| 第 1 层 | `~/.codex/AGENTS.md` 中的规则块 | 每次对话始终加载 | 核心可视化规则 |
| 第 2 层 | `SKILL.md` 完整内容 | 按需加载 | 详细场景对照、四组对比示范 |

## 与 de-gpt-ify 的关系

两个 skill 互补，各自独立：
- **de-gpt-ify**：解决"怎么说话"（语言风格）
- **show-dont-tell**：解决"怎么呈现"（输出格式）

两个 skill 的 install.sh 各自往 AGENTS.md 写入自己的规则块（用不同的标记注释），互不干扰。
