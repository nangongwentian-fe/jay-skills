---
name: browser-mcp-resource-guard
description: Use when Codex is about to use, is using, or has just used browser automation MCP tools such as chrome-devtools-mcp, Chrome DevTools MCP, Playwright MCP, @playwright/mcp, browser MCP, or browser/computer automation helpers; when the user mentions high CPU, high energy usage, battery drain, fans, heat, lag, duplicate browser MCP processes, stale Chrome Helper processes, or MCP cleanup; or when long-running Codex sessions may leave browser automation MCP helper processes behind.
---

# Browser MCP Resource Guard

## Goal

Reduce CPU, memory, battery, and fan impact from browser automation MCP tools without breaking active work. Treat cleanup as a guarded operation: inspect first, report clearly, and only kill processes when it is safe or explicitly requested.

## Decision Rules

- Prefer not using browser MCP when static checks, local files, tests, builds, or ordinary HTTP requests answer the task.
- Use Chrome DevTools MCP when the task needs live browser state, console messages, network requests, DOM snapshots, screenshots, viewport checks, or real interactions.
- Use browser MCP in focused batches: open the page, collect needed evidence, close or stop related local services when finished.
- Avoid repeated screenshots, repeated new tabs, performance traces, heap snapshots, and attaching to a Chrome profile with many tabs unless the task requires them.
- After browser MCP use, run a read-only process check when the session was long, multiple pages/tools were used, or the user mentions energy/resource problems.

## Read-Only Check

Run the bundled report script from the skill directory:

```bash
scripts/browser_mcp_process_report.sh
```

If the script is unavailable, use:

```bash
ps -axo pid=,ppid=,rss=,etime=,command= \
  | rg 'chrome-devtools-mcp|@playwright/mcp|playwright-mcp|ms-playwright|mcp-chrome'
```

Report:

- number of browser MCP-related process rows
- rough RSS total
- longest elapsed time
- whether there are duplicate stacks
- whether any process appears related to the current task

## Cleanup Policy

- Do not blindly kill all MCP processes.
- Ask before killing when a process may belong to another active thread, browser task, IDE session, or user workflow.
- It is usually safe to propose cleanup when there are multiple duplicate `chrome-devtools-mcp` or Playwright MCP stacks, old elapsed times, no current browser automation work, and the user is reporting energy or lag.
- Prefer terminating only browser MCP helper processes, not the user's normal Chrome profile.

Use these commands only after approval or when the user explicitly asks to clean clear browser MCP leftovers:

```bash
pkill -f 'chrome-devtools-mcp'
pkill -f '@playwright/mcp'
pkill -f 'playwright-mcp'
```

For a current-turn dev server started by Codex, stop the specific shell session or process instead of using broad `pkill`.

## Final Response

State the result in one or two short sections:

- what was found, with process count/RSS if checked
- what was cleaned or what should be cleaned
- any remaining risk, such as possible active browser automation in another thread
