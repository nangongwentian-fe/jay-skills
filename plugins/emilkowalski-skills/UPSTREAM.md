# Upstream

本插件打包 [emilkowalski/skills](https://github.com/emilkowalski/skills) 的 `skills/` 目录，供 Codex marketplace 安装。

| 项目 | 值 |
|------|----|
| 上游提交 | `6bf24434f7730ad169077756cf9c7cd7bd675fc6` |
| 同步日期 | 2026-07-20 |
| 许可证 | MIT，见 [`LICENSE`](./LICENSE) |

## 本地兼容补丁

`review-animations` 上游使用 Claude 专属的 `disable-model-invocation` frontmatter。同步时删除该字段，使 skill 通过 Codex 校验；正文不变。
