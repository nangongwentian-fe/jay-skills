#!/usr/bin/env bash
# check_updates.sh — 检测 nangongwentian-fe/Awesome-GlobalRule 是否有新提交
# 输出: "up-to-date:<sha>:<date>" 或 "updates-available:<new_sha>:<commit_message>:<date>"
# 退出码: 0=有更新, 1=已是最新, 2=错误

set -euo pipefail

REPO="nangongwentian-fe/Awesome-GlobalRule"
STATE_FILE="${HOME}/.claude/.sync_state.json"

# 检查 gh CLI
if ! command -v gh &>/dev/null; then
  echo "ERROR: gh CLI not found. Install from https://cli.github.com" >&2
  exit 2
fi

# 获取远程最新 commit 信息
REMOTE_INFO=$(gh api "repos/${REPO}/commits/main" \
  --jq '{sha: .sha, message: .commit.message, date: .commit.committer.date}' 2>/dev/null) || {
  echo "ERROR: Failed to fetch remote info. Run: gh auth status" >&2
  exit 2
}

REMOTE_SHA=$(echo "$REMOTE_INFO" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['sha'])")
REMOTE_MSG=$(echo "$REMOTE_INFO" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['message'].split('\n')[0])")
REMOTE_DATE=$(echo "$REMOTE_INFO" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['date'])")

# 读取本地记录的 SHA
LOCAL_SHA=""
if [[ -f "$STATE_FILE" ]]; then
  LOCAL_SHA=$(python3 -c "import json; d=json.load(open('${STATE_FILE}')); print(d.get('sha',''))" 2>/dev/null || echo "")
fi

if [[ "$LOCAL_SHA" == "$REMOTE_SHA" ]]; then
  echo "up-to-date:${REMOTE_SHA}:${REMOTE_DATE}"
  exit 1
else
  echo "updates-available:${REMOTE_SHA}:${REMOTE_MSG}:${REMOTE_DATE}"
  exit 0
fi
