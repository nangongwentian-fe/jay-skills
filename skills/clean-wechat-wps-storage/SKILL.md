---
name: clean-wechat-wps-storage
description: Clean local disk usage from WeChat/微信 and WPS Office on macOS. Use when the user says WeChat, Weixin, 微信, WPS, or WPS Office takes too much space, asks what can be cleaned, wants to clear chat records, chat images, videos, emojis, caches, cloud-document caches, plugins, fonts, logs, or wants an interview-confirm-plan-clean workflow before moving app data to Trash.
---

# Clean WeChat And WPS Storage

Use this skill for macOS storage cleanup of WeChat and WPS Office. Always protect user data by scanning first, interviewing for cleanup scope, presenting a plan, and waiting for explicit confirmation before moving anything.

## Workflow

1. Run a read-only scan:
   ```bash
   python3 scripts/wechat_wps_storage.py scan --format markdown
   ```
2. Interview the user before planning. Ask only about scopes that exist and have non-trivial size.
3. Present a cleanup plan with:
   - target items and sizes
   - data impact
   - estimated total moved to Trash
   - rollback location and validation steps
4. Do not clean until the user explicitly confirms the plan.
5. After confirmation, run a dry run with the selected item IDs:
   ```bash
   python3 scripts/wechat_wps_storage.py move-to-trash --ids <id> <id>
   ```
6. If the dry run matches the confirmed plan, execute:
   ```bash
   python3 scripts/wechat_wps_storage.py move-to-trash --stop-apps --execute --ids <id> <id>
   ```
7. Re-run scan and report before/after sizes. Tell the user the Trash backup path and that disk space is not fully reclaimed until Trash is emptied.

## Cleanup Scope Rules

Use these defaults when the user is unsure:

| Scope | Default | Impact |
| --- | --- | --- |
| Low-risk caches | Recommend | Temporary files, logs, and app caches are recreated. |
| Runtime/plugin data | Ask | First use may redownload plugins or web runtimes. |
| WPS cloud file cache | Ask | Local cached cloud files are removed; cloud copies should remain if synced. |
| WeChat chat media | Ask | Local images, files, videos, emojis, and previews may need redownloading or may disappear locally. |
| WeChat chat account | High-risk ask | Local chat history, search, attachments, emojis, and videos for that account are removed from this Mac. |
| WeChat database only | Avoid unless requested | Removing databases without media is rarely useful and can break local history. |

Never delete app bundles in `/Applications` unless the user asks to uninstall the app. Never permanently delete app data directly; move it to `~/.Trash/app-cleanup-YYYYMMDD-HHMMSS/`.

## Interview Prompts

Ask concise questions in Chinese. Use concrete choices:

- "只清缓存和日志，还是也清插件/运行时缓存？"
- "WPS 云文档本地缓存要清吗？清之前请确认云端已有文件。"
- "微信聊天数据要怎么处理：只清聊天媒体，还是删除本机这个账号的聊天记录？"
- "如果有多个微信账号目录，逐个列出大小并让用户选择账号。"

If the user already states the desired scope, do not re-ask. State the assumption in the plan.

## Safety Checklist

Before executing cleanup:

- Confirm all selected item IDs came from `scan`.
- Confirm the plan says "move to Trash", not permanent delete.
- Stop WeChat and WPS before moving files.
- Preserve original path structure under the Trash backup directory.
- After moving, launch apps only for a basic start check; do not claim full validation of login, cloud sync, or message sending unless actually verified.

## Rollback

If the user reports a problem before emptying Trash, restore by moving the affected directory from the backup path to its original path. Stop WeChat and WPS before restoring. Use the preserved path under the backup directory to identify the exact original location.
