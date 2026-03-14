---
name: sync-global-rules
description: >
  同步 nangongwentian-fe/Awesome-GlobalRule 仓库到本地 AI 编程工具配置。
  当用户说"同步规则"、"同步 global rule"、"检查规则更新"、"更新 agent rules"、
  "sync global rules"、"规则有没有更新"、"拉取最新规则"时，立即使用此 skill。
  同步目标：Claude Code (~/.claude/) 和 Codex (~/.codex/)。
  包含自动备份、更新检测、状态追踪功能。
---

# sync-global-rules

将 GitHub 仓库 `nangongwentian-fe/Awesome-GlobalRule` 中的 Agent 规则体系同步到本地两个 AI 工具的全局配置目录。

## 同步映射

| 仓库来源 | Claude Code 目标 | Codex 目标 |
|----------|-----------------|------------|
| `AGENTS.md` | `~/.claude/CLAUDE.md` | `~/.codex/AGENTS.md` |
| `docs/agent-rules/*` (11 个文件) | `~/.claude/docs/agent-rules/` | `~/.codex/docs/agent-rules/` |

## 状态追踪

上次同步信息保存在 `~/.claude/.sync_state.json`，包含已同步的 commit SHA。
这样每次检查时只需对比 SHA，不用下载全部内容。

## 工作流程

### 场景一：检查是否有更新（推荐先执行）

```bash
bash ~/.claude/skills/sync-global-rules/scripts/check_updates.sh
```

**输出解读：**
- 退出码 `0` + 输出以 `updates-available:` 开头 → 有新版本，执行同步
- 退出码 `1` + 输出以 `up-to-date:` 开头 → 已是最新，无需操作
- 退出码 `2` + 输出 `ERROR:` → 环境问题（gh 未安装或未登录）

### 场景二：执行完整同步

有更新时（或用户明确要求同步时）：

```bash
bash ~/.claude/skills/sync-global-rules/scripts/sync.sh
```

脚本会自动：
1. 检查远程 SHA 与本地记录的 SHA
2. 在 `~/.claude/backups/<timestamp>/` 自动备份现有文件
3. 下载所有文件并写入两个目标目录
4. 更新 `~/.claude/.sync_state.json`

### 场景三：强制同步（即使 SHA 一致）

```bash
bash ~/.claude/skills/sync-global-rules/scripts/sync.sh --force
```

### 场景四：预览模式（不写入文件）

```bash
bash ~/.claude/skills/sync-global-rules/scripts/sync.sh --dry-run
```

## 标准执行顺序

当用户触发此 skill 时，按以下顺序执行：

1. 运行 `check_updates.sh`
2. 解读输出：
   - 有更新 → 告知用户"发现新版本：<commit message>"，询问是否同步（或直接同步，视用户指令）
   - 已最新 → 告知用户"当前已是最新（SHA: <short_sha>，上次同步: <date>）"，结束
   - 错误 → 告知用户具体错误并给出修复建议
3. 有更新时，运行 `sync.sh`
4. 汇报同步结果（SHA、备份路径、文件数量）

## 前提条件

- `gh` CLI 已安装且已登录（`gh auth status`）
- `python3` 可用
- 对 `~/.claude/` 和 `~/.codex/` 有写权限

## 注意事项

- 同步会覆盖现有规则文件，但 **每次同步前都会自动备份**（保存于 `~/.claude/backups/`）
- 备份仅保存主规则文件（`CLAUDE.md` 和 `AGENTS.md`），docs 目录文件不备份（可从 GitHub 恢复）
- 如用户有本地个人化修改（如语言偏好等），同步后需手动追加
