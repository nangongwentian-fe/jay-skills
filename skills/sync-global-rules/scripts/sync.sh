#!/usr/bin/env bash
# sync.sh — 从 nangongwentian-fe/Awesome-GlobalRule 同步规则到本地
#
# 用法:
#   bash sync.sh              # 正常同步
#   bash sync.sh --force      # 强制同步（跳过 SHA 检查）
#   bash sync.sh --dry-run    # 仅预览，不写入文件
#
# 目标路径:
#   ~/.claude/CLAUDE.md + ~/.claude/docs/agent-rules/
#   ~/.codex/AGENTS.md  + ~/.codex/docs/agent-rules/

set -euo pipefail

REPO="nangongwentian-fe/Awesome-GlobalRule"
STATE_FILE="${HOME}/.claude/.sync_state.json"
BACKUP_DIR="${HOME}/.claude/backups"
FORCE=false
DRY_RUN=false

# 解析参数
for arg in "$@"; do
  case $arg in
    --force)   FORCE=true ;;
    --dry-run) DRY_RUN=true ;;
  esac
done

# 检查依赖
for cmd in gh python3; do
  if ! command -v "$cmd" &>/dev/null; then
    echo "ERROR: '$cmd' not found." >&2
    exit 1
  fi
done

# base64 解码（兼容 macOS/Linux）
decode_base64() {
  if base64 --version 2>&1 | grep -q GNU; then
    base64 -d
  else
    base64 -D  # macOS
  fi
}

# 获取远程文件内容
fetch_file() {
  local path="$1"
  gh api "repos/${REPO}/contents/${path}" --jq '.content' | tr -d '\n' | decode_base64
}

# 写入文件（dry-run 模式下只打印）
write_file() {
  local content="$1"
  local target="$2"
  if [[ "$DRY_RUN" == true ]]; then
    echo "  [DRY-RUN] Would write: $target"
  else
    echo "$content" > "$target"
    echo "  ✓ $target"
  fi
}

# ─── 检查是否需要更新 ───────────────────────────────────────────────────────────
echo "🔍 检查远程仓库状态..."
REMOTE_INFO=$(gh api "repos/${REPO}/commits/main" \
  --jq '{sha: .sha, message: .commit.message, date: .commit.committer.date}')
REMOTE_SHA=$(echo "$REMOTE_INFO" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['sha'])")
REMOTE_MSG=$(echo "$REMOTE_INFO" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['message'].split('\n')[0])")
REMOTE_DATE=$(echo "$REMOTE_INFO" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['date'])")

LOCAL_SHA=""
LAST_SYNC=""
if [[ -f "$STATE_FILE" ]]; then
  LOCAL_SHA=$(python3 -c "import json; d=json.load(open('${STATE_FILE}')); print(d.get('sha',''))" 2>/dev/null || echo "")
  LAST_SYNC=$(python3 -c "import json; d=json.load(open('${STATE_FILE}')); print(d.get('synced_at','未知'))" 2>/dev/null || echo "未知")
fi

echo "  远程最新: ${REMOTE_SHA:0:8} — ${REMOTE_MSG} (${REMOTE_DATE})"
if [[ -n "$LOCAL_SHA" ]]; then
  echo "  本地记录: ${LOCAL_SHA:0:8} (上次同步: ${LAST_SYNC})"
else
  echo "  本地记录: 无（首次同步）"
fi

if [[ "$LOCAL_SHA" == "$REMOTE_SHA" && "$FORCE" != true ]]; then
  echo ""
  echo "✅ 已是最新，无需同步。使用 --force 可强制同步。"
  exit 0
fi

if [[ "$LOCAL_SHA" == "$REMOTE_SHA" && "$FORCE" == true ]]; then
  echo "  ⚡ 强制同步模式"
fi

# ─── 备份现有文件 ──────────────────────────────────────────────────────────────
if [[ "$DRY_RUN" != true ]]; then
  BACKUP_TS=$(date +%Y%m%d_%H%M%S)
  BACKUP_PATH="${BACKUP_DIR}/${BACKUP_TS}"
  mkdir -p "$BACKUP_PATH"

  [[ -f "${HOME}/.claude/CLAUDE.md" ]] && cp "${HOME}/.claude/CLAUDE.md" "${BACKUP_PATH}/CLAUDE.md"
  [[ -f "${HOME}/.codex/AGENTS.md" ]] && cp "${HOME}/.codex/AGENTS.md" "${BACKUP_PATH}/AGENTS.md"
  echo ""
  echo "📦 已备份现有文件到: ${BACKUP_PATH}"
fi

# ─── 创建目录 ─────────────────────────────────────────────────────────────────
if [[ "$DRY_RUN" != true ]]; then
  mkdir -p "${HOME}/.claude/docs/agent-rules"
  mkdir -p "${HOME}/.codex/docs/agent-rules"
fi

# ─── 同步主规则文件 ────────────────────────────────────────────────────────────
echo ""
echo "📥 同步主规则文件..."
MAIN_CONTENT=$(fetch_file "AGENTS.md")
write_file "$MAIN_CONTENT" "${HOME}/.claude/CLAUDE.md"
write_file "$MAIN_CONTENT" "${HOME}/.codex/AGENTS.md"

# ─── 同步 docs/agent-rules/ ───────────────────────────────────────────────────
echo ""
echo "📥 同步 docs/agent-rules/..."
FILES=(
  README.md
  code-organization.md
  code-review.md
  coding-style.md
  component-design.md
  imports-and-paths.md
  local-agents-template.md
  memory-scoping.md
  memory-system.md
  memory-update-and-pruning.md
  subagent-strategy.md
)

for FILE in "${FILES[@]}"; do
  CONTENT=$(fetch_file "docs/agent-rules/${FILE}")
  write_file "$CONTENT" "${HOME}/.claude/docs/agent-rules/${FILE}"
  write_file "$CONTENT" "${HOME}/.codex/docs/agent-rules/${FILE}"
done

# ─── 更新状态文件 ─────────────────────────────────────────────────────────────
if [[ "$DRY_RUN" != true ]]; then
  SYNC_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  python3 -c "
import json
state = {
    'sha': '${REMOTE_SHA}',
    'commit_message': '${REMOTE_MSG}',
    'synced_at': '${SYNC_TIME}',
    'repo': '${REPO}'
}
with open('${STATE_FILE}', 'w') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)
print('  ✓ 状态已更新: ${STATE_FILE}')
"
fi

echo ""
echo "✅ 同步完成！"
echo "   SHA: ${REMOTE_SHA:0:8} — ${REMOTE_MSG}"
echo "   Claude Code: ~/.claude/CLAUDE.md + ~/.claude/docs/agent-rules/ (11 files)"
echo "   Codex:       ~/.codex/AGENTS.md  + ~/.codex/docs/agent-rules/ (11 files)"
