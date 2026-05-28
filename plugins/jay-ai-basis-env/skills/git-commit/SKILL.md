---
name: git-commit
description: 基于当前 git 工作区变更生成并创建单个提交。用于用户要求“帮我提交代码”“根据当前 diff 生成 commit”“创建一次 git commit”“整理 staged/unstaged 变更并提交”，或明确提供 `git status`、`git diff HEAD`、当前分支和最近提交记录时。适用于需要分析改动、编写结构化 commit message，并执行 `git add` 和 `git commit` 的场景。
---

# Git Commit

基于当前工作区的 staged、unstaged 和 untracked 变更，生成一个能够真实概括改动范围的单次 git commit，并直接执行提交。

## 执行原则

- 先判断当前变更是否能被诚实地概括为一个 commit。
- 优先使用用户已经提供的 `git status`、`git diff HEAD`、当前分支和最近提交记录；缺失时再自行补充读取。
- 除非用户明确限制范围，否则默认提交当前工作区全部相关变更，使用 `git add -A`。
- 不要顺手修改代码、不要运行测试、不要清理无关文件、不要做额外格式化。
- 不要 `amend`、不要拆分为多个 commit、不要 push，除非用户明确要求。
- 如果没有可提交变更，直接说明不能创建 commit，不要创建空提交。
- 如果变更明显包含两个以上互不相关的主题，先指出不能安全地合并成一个 commit，而不是编造含糊的 message。

## 标准流程

### 1. 收集上下文

- 优先消费用户消息中已给出的 git 信息。
- 如果上下文不完整，再补充运行必要命令：
  - `git status`
  - `git diff HEAD`
  - `git branch --show-current`
  - `git log --oneline -10`

### 2. 归纳改动意图

- 提炼本次提交的单一主题。
- 识别 2 到 5 个最重要的改动点，写入 commit body。
- 优先描述“结果”和“行为变化”，不要只罗列文件名。

### 3. 生成 commit message

- 标题使用 Conventional Commit 前缀，例如：`feat`、`fix`、`refactor`、`docs`、`chore`、`test`、`build`。
- 标题必须具体，能概括全部改动，不写空泛词如“update files”。
- body 使用中文项目符号，每条单独成段，尽量写成用户可理解的结果描述。

## Commit Message 模板

默认使用这个结构，并保持空行风格一致：

```text
type: 简明概括本次改动

- 改动点 1

- 改动点 2

- 改动点 3
```

如果改动非常小，允许只保留 1 到 2 条要点，但不要省略标题。

## 执行约束

- 对支持工具调用的环境，在同一次回复里完成 stage 和 commit。
- 如果用户明确要求“不要输出任何文字，只输出工具调用”，严格遵守，不要发送额外解释。
- 优先使用非交互式提交方式，确保多行 commit message 可以稳定写入。
- 默认命令顺序是先 `git add -A`，再 `git commit`。
- 如果用户明确指定“只提交已暂存内容”或“只提交某些文件”，按用户范围执行，不要扩大提交范围。

## 推荐命令模式

当环境允许一条 shell 命令完成时，优先使用非交互式方式写入多行 message，例如：

```bash
git add -A && git commit -F - <<'EOF'
feat: 示例标题

- 要点 1

- 要点 2
EOF
```

如果工具系统支持一条消息内发送多个顺序工具调用，也可以分别执行 `git add -A` 和 `git commit`，但不要夹带额外文本。

## 示例

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
