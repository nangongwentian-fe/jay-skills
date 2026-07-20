# Upstream

本插件打包 [xxxily/code-honor-skill](https://github.com/xxxily/code-honor-skill) 的 `skills/code-honor/` 目录，供 Codex marketplace 安装。

| 项目 | 值 |
|------|----|
| 上游提交 | `f5826ca60b7074b79d6a50adb449151f8c8219ba` |
| 同步日期 | 2026-07-20 |
| 许可证 | MIT，见 [`LICENSE`](./LICENSE) |

## 本地兼容修正

移除了 `scripts/code_conduct_analyzer.py` 文件开头误包裹的 Markdown 标题和代码围栏，使其可作为 Python 脚本直接执行；扫描逻辑未修改。
