# 图片资产协议

用清单管理图片资产，让图片路径稳定、可检查、可复用。

## 最小清单

```json
{
  "deck": {
    "title": "Quarterly AI Operations Review",
    "audience": "executive team"
  },
  "assets": [
    {
      "id": "cover-hero",
      "kind": "hero-image",
      "path": "assets/imagegen/cover-hero.png",
      "aspectRatio": "16:9",
      "alt": "Enterprise AI operations room with dark empty space on the left",
      "usage": "cover background",
      "safeZone": "left",
      "prompt": "premium enterprise AI operations workspace, cinematic but realistic, dark negative space on the left, 16:9, no text, no logo, no watermark"
    }
  ]
}
```

## 字段

| 字段 | 必填 | 用途 |
| --- | --- | --- |
| `id` | 是 | 幻灯片引用图片时使用的稳定标识。 |
| `kind` | 是 | `hero-image`、`section-background`、`scene-image`、`texture` 或 `cutout`。 |
| `path` | 是 | 相对项目的图片路径。 |
| `aspectRatio` | 是 | `16:9`、`4:3` 或 `1:1`。 |
| `alt` | 是 | 便于审核和无障碍使用的图片描述。 |
| `usage` | 建议 | 图片会用在哪类页面。 |
| `safeZone` | 建议 | 适合放文字的区域：`left`、`right`、`top`、`bottom`、`center` 或 `none`。 |
| `prompt` | 建议 | 生成提示词，便于复查和重新生成。 |
| `minWidth` / `minHeight` | 可选 | 覆盖默认尺寸阈值。 |

## 页面引用

页面应该通过 `assetId` 引用图片，不要在每页复制临时图片路径。

```json
{
  "type": "image-split",
  "title": "Automation quality improved after asset validation",
  "body": "Native text remains editable while the visual system carries tone.",
  "image": {
    "assetId": "automation-scene",
    "placement": "right-frame",
    "cropFocus": "center"
  }
}
```

## 提示词公式

```text
[品质/风格] + [行业主体] + [构图/安全区] + [比例] + no text, no logo, no watermark
```

示例：

| 用途 | 提示词形态 |
| --- | --- |
| 封面 | `premium enterprise cyber operations room, dark negative space on the left, 16:9, no text, no logo` |
| 章节页 | `minimal premium abstract supply-chain data texture, calm center area, 16:9, no text, no logo` |
| 内容页场景图 | `realistic enterprise document automation scene, clean desk, 4:3, no readable text, no logo` |

## 拒绝规则

出现这些情况时拒绝或重新生成图片：

| 问题 | 原因 |
| --- | --- |
| 比例错误 | 裁切结果不可控。 |
| 有可读假文字 | 会和 PPT 原生文字冲突。 |
| 明显商标或水印 | 有法律和品牌风险。 |
| 安全区细节太多 | 标题对比度容易失败。 |
| 分辨率太低 | 大屏展示会显得粗糙。 |
