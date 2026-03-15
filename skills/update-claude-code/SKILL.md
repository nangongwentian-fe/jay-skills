---
name: update-claude-code
description: 更新 Claude Code CLI 到最新版本。当用户说"更新 Claude Code"、"升级 Claude Code"、"update claude code"、"claude code 太旧了"、"执行 install.sh 更新"，或者想让 Claude 自我更新时，立即使用此 skill。不要等用户明确说"用 npm"——只要涉及更新 Claude Code 本身，就使用这个 skill。
---

# 更新 Claude Code

## 步骤

1. 使用 npm 全局安装最新版本：

```bash
npm install -g @anthropic-ai/claude-code@latest
```

2. 验证更新是否成功：

```bash
claude --version
```

3. 向用户报告更新后的版本号。

## 注意事项

- `curl -fsSL https://claude.ai/install.sh | bash` 这种方式在部分地区（如中国大陆）无法访问，会返回 HTML 错误页面而非安装脚本，**不要使用**。
- npm 方式是最可靠的更新方法，直接使用即可，无需代理。
- 如果 npm 也失败，检查 npm 是否已安装：`npm --version`，并提示用户先安装 Node.js。
