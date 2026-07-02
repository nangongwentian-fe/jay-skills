#!/usr/bin/env bash
set -euo pipefail

pattern="${1:-chrome-devtools-mcp|@playwright/mcp|playwright-mcp|ms-playwright|mcp-chrome}"

rows="$(
  ps -axo pid=,ppid=,rss=,etime=,command= \
    | grep -E "$pattern" \
    | grep -v 'grep -E' \
    | grep -v 'browser_mcp_process_report.sh' \
    || true
)"

if [ -z "$rows" ]; then
  echo "No browser MCP-related processes found."
  exit 0
fi

echo "$rows"

count="$(printf '%s\n' "$rows" | awk 'NF { count += 1 } END { print count + 0 }')"
rss_kb="$(printf '%s\n' "$rows" | awk 'NF { sum += $3 } END { print sum + 0 }')"
rss_mib="$(awk -v kb="$rss_kb" 'BEGIN { printf "%.1f", kb / 1024 }')"

echo
echo "Process rows: $count"
echo "Total RSS: ${rss_mib} MiB"
