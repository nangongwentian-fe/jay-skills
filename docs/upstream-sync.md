# 上游插件同步

本仓库定期检查三个外部 skill 仓库。发现新提交后，同步对应插件并创建独立 PR；主分支不会被定时任务直接修改。

## 摘要

| 插件 | 上游路径 | 本地处理 |
|------|----------|----------|
| `taste-skill` | `skills/`、`LICENSE` | 原样镜像 |
| `code-honor-skill` | `skills/code-honor/`、`LICENSE` | 重放 Python 扫描器兼容补丁 |
| `andrej-karpathy-skills` | `skills/karpathy-guidelines/` | 原样镜像；上游无独立许可证文件 |

机器可读来源位于各插件的 `upstream.json`，人工可读来源位于 `UPSTREAM.md`。同步 PR 按插件拆分，必须人工审查后合并。

## 常用操作

检查所有上游仓库，不修改文件：

```bash
python scripts/sync_upstream_plugins.py check
```

同步指定插件：

```bash
python scripts/sync_upstream_plugins.py sync --plugin taste-skill
```

重新生成指定插件，即使提交号没有变化：

```bash
python scripts/sync_upstream_plugins.py sync --plugin code-honor-skill --force
```

验证本地 marketplace、插件清单、skill frontmatter、Python 语法和来源记录：

```bash
python scripts/validate_plugins.py
python -m unittest discover -s tests -p "test_*.py"
```

## 自动执行

`.github/workflows/sync-upstream-plugins.yml` 每周一 UTC 03:17 运行，也支持在 GitHub Actions 页面手动触发。每个插件在独立矩阵任务中执行：

1. 查询上游 `main` 分支最新 SHA。
2. 在临时目录浅克隆仓库。
3. 只复制 `upstream.json` 声明的路径并拒绝符号链接。
4. 在临时快照中检查并应用本地补丁。
5. 更新来源 SHA、同步日期和插件 cachebuster 版本。
6. 验证全部 marketplace 插件。
7. 有改动时创建或更新 `automation/sync-<plugin>` PR。

workflow 需要：

```yaml
permissions:
  contents: write
  pull-requests: write
```

GitHub 仓库还需允许 Actions 创建 PR。禁止自动审批和自动合并；上游 `SKILL.md` 与脚本属于需要审查的可执行输入。

## 本地补丁

`code-honor-skill` 上游将 Python 文件误包在 Markdown 标题与代码围栏中。本仓使用 `patches/fix-analyzer-wrapper.patch` 删除包装，不修改扫描逻辑。

同步时先执行 `git apply --check`。如果上游修改导致补丁失效，同步任务会失败，必须人工确认新版上游是否仍需该补丁，不能静默跳过。

## 合并后更新 Codex

先升级 marketplace，再重新安装发生变化的插件：

```bash
codex plugin marketplace upgrade jay-skills
codex plugin add <plugin-name>@jay-skills
```

插件版本包含上游 SHA，例如 `1.0.0+codex.upstream-7c397f22d3af`。重新安装后使用新任务验证，避免旧任务继续使用缓存的 skill。
