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

4. **清理旧版本**：检查本机是否存在多个 Claude Code 版本残留，如有则只保留最新版本：

```bash
# 检查本地版本目录
ls ~/.local/share/claude/versions/

# 获取当前 symlink 指向的版本
readlink ~/.local/bin/claude
```

如果存在多个版本目录，**不要只改 symlink**——自动回滚机制会把 symlink 改回去。正确做法是通过 npm 安装来彻底绕开这套机制：

```bash
npm install -g @anthropic-ai/claude-code@latest
```

npm 安装的版本路径（通常为 `~/.nvm/versions/node/vX.X.X/bin/claude` 或系统 npm bin）在 PATH 中优先级高于 `~/.local/bin/claude`，可完全绕开自动回滚机制。

安装完成后，清理旧版本目录：

```bash
# 删除全部版本残留目录
rm -rf ~/.local/share/claude/versions/
```

再次验证版本正确：

```bash
claude --version && which claude
```

确认 `which claude` 输出的是 npm 路径（如 `~/.nvm/...`），而不是 `~/.local/bin/claude`。

## 注意事项

- `curl -fsSL https://claude.ai/install.sh | bash` 这种方式在部分地区（如中国大陆）无法访问，会返回 HTML 错误页面而非安装脚本，**不要使用**。
- npm 方式是最可靠的更新方法，直接使用即可，无需代理。
- 如果 npm 也失败，检查 npm 是否已安装：`npm --version`，并提示用户先安装 Node.js。
- Claude Code 使用自动更新机制，会将各版本下载到 `~/.local/share/claude/versions/` 目录，`~/.local/bin/claude` 是一个 symlink。当新版本崩溃时会自动回滚 symlink 到旧版本，导致 `--version` 显示的版本低于预期。**仅修改 symlink 无法解决问题**，回滚机制会重新下载旧版并改回去。必须通过 npm 安装来绕开这套机制。
- 清理 `~/.local/share/claude/versions/` 目录后，npm 安装的版本不受影响，仍可正常使用。
