#!/bin/bash
# show-dont-tell installer
# 将信息可视化规则写入 ~/.codex/AGENTS.md

set -e

AGENTS_MD="${HOME}/.codex/AGENTS.md"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RULES_FILE="${SCRIPT_DIR}/../references/agents-md-rules.md"
MARKER="show-dont-tell:start"

if [ ! -f "$RULES_FILE" ]; then
    echo "错误：找不到规则文件 $RULES_FILE"
    exit 1
fi

mkdir -p "$(dirname "$AGENTS_MD")"

if [ "$1" = "--uninstall" ]; then
    if [ -f "$AGENTS_MD" ] && grep -q "$MARKER" "$AGENTS_MD"; then
        sed -i '' '/<!-- show-dont-tell:start -->/,/<!-- show-dont-tell:end -->/d' "$AGENTS_MD"
        echo "✓ 已从 $AGENTS_MD 移除 show-dont-tell 规则。"
    else
        echo "未找到 show-dont-tell 规则，无需移除。"
    fi
    exit 0
fi

if [ -f "$AGENTS_MD" ] && grep -q "$MARKER" "$AGENTS_MD"; then
    echo "✓ show-dont-tell 规则已存在于 $AGENTS_MD，跳过写入。"
    echo "  如需更新，先运行: $0 --uninstall"
    exit 0
fi

echo "" >> "$AGENTS_MD"
cat "$RULES_FILE" >> "$AGENTS_MD"
echo "" >> "$AGENTS_MD"

echo "✓ show-dont-tell 规则已写入 $AGENTS_MD"
echo "  现在 Codex 中的 GPT 会优先用表格、代码块、列表等格式呈现信息。"
echo "  卸载: $0 --uninstall"
