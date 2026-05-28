#!/bin/bash
# de-gpt-ify installer
# 将中文风格规则写入 ~/.codex/AGENTS.md，让 Codex 中的 GPT 始终遵守

set -e

AGENTS_MD="${HOME}/.codex/AGENTS.md"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RULES_FILE="${SCRIPT_DIR}/../references/agents-md-rules.md"
MARKER="de-gpt-ify:start"

if [ ! -f "$RULES_FILE" ]; then
    echo "错误：找不到规则文件 $RULES_FILE"
    exit 1
fi

mkdir -p "$(dirname "$AGENTS_MD")"

if [ -f "$AGENTS_MD" ] && grep -q "$MARKER" "$AGENTS_MD"; then
    echo "✓ de-gpt-ify 规则已存在于 $AGENTS_MD，跳过写入。"
    echo "  如需更新，先运行: $0 --uninstall"
    exit 0
fi

if [ "$1" = "--uninstall" ]; then
    if [ -f "$AGENTS_MD" ] && grep -q "$MARKER" "$AGENTS_MD"; then
        sed -i '' '/<!-- de-gpt-ify:start -->/,/<!-- de-gpt-ify:end -->/d' "$AGENTS_MD"
        echo "✓ 已从 $AGENTS_MD 移除 de-gpt-ify 规则。"
    else
        echo "未找到 de-gpt-ify 规则，无需移除。"
    fi
    exit 0
fi

echo "" >> "$AGENTS_MD"
cat "$RULES_FILE" >> "$AGENTS_MD"
echo "" >> "$AGENTS_MD"

echo "✓ de-gpt-ify 规则已写入 $AGENTS_MD"
echo "  现在 Codex 中的 GPT 会自动遵守中文风格规则。"
echo "  卸载: $0 --uninstall"
