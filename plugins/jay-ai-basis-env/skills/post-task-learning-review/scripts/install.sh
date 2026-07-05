#!/bin/bash
# post-task-learning-review installer
# 将任务后经验维护规则写入 ~/.codex/AGENTS.md

set -e

AGENTS_MD="${HOME}/.codex/AGENTS.md"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RULES_FILE="${SCRIPT_DIR}/../references/agents-md-rules.md"
MARKER="post-task-learning-review:start"

remove_block() {
    if sed --version >/dev/null 2>&1; then
        sed -i '/<!-- post-task-learning-review:start -->/,/<!-- post-task-learning-review:end -->/d' "$AGENTS_MD"
    else
        sed -i '' '/<!-- post-task-learning-review:start -->/,/<!-- post-task-learning-review:end -->/d' "$AGENTS_MD"
    fi
}

if [ ! -f "$RULES_FILE" ]; then
    echo "错误：找不到规则文件 $RULES_FILE"
    exit 1
fi

mkdir -p "$(dirname "$AGENTS_MD")"

if [ "$1" = "--uninstall" ]; then
    if [ -f "$AGENTS_MD" ] && grep -q "$MARKER" "$AGENTS_MD"; then
        remove_block
        echo "✓ 已从 $AGENTS_MD 移除 post-task-learning-review 规则。"
    else
        echo "未找到 post-task-learning-review 规则，无需移除。"
    fi
    exit 0
fi

if [ -f "$AGENTS_MD" ] && grep -q "$MARKER" "$AGENTS_MD"; then
    echo "✓ post-task-learning-review 规则已存在于 $AGENTS_MD，跳过写入。"
    echo "  如需更新，先运行: $0 --uninstall"
    exit 0
fi

echo "" >> "$AGENTS_MD"
cat "$RULES_FILE" >> "$AGENTS_MD"
echo "" >> "$AGENTS_MD"

echo "✓ post-task-learning-review 规则已写入 $AGENTS_MD"
echo "  现在 Codex 会在非平凡任务结束后主动判断经验是否应维护到项目文档、memory 或 skill。"
echo "  卸载: $0 --uninstall"
