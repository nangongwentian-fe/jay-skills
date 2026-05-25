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
      "reuseScope": "deck",
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
| `kind` | 是 | `hero-image`、`section-background`、`scene-image`、`texture`、`cutout`、`flow-line`、`flow-node`、`marker` 或 `icon-asset`。 |
| `path` | 是 | 相对项目的图片路径。 |
| `aspectRatio` | 是 | `16:9`、`4:3`、`1:1`，也可以是 `8:1`、`12:1` 这类组件比例。 |
| `alt` | 是 | 便于审核和无障碍使用的图片描述。 |
| `usage` | 建议 | 图片会用在哪类页面。 |
| `safeZone` | 建议 | 适合放文字的区域：`left`、`right`、`top`、`bottom`、`center` 或 `none`。 |
| `prompt` | 建议 | 生成提示词，便于复查和重新生成。 |
| `minWidth` / `minHeight` | 可选 | 覆盖默认尺寸阈值。 |
| `componentRole` | 组件建议 | `background`、`scene`、`line`、`node`、`marker`、`icon`、`decoration`。 |
| `componentFamily` | 组件建议 | 同一组可复用组件的族名，例如 `blue-process`。 |
| `variant` | 组件建议 | `default`、`active`、`warning`、`disabled` 等状态。 |
| `reuseScope` | 建议 | `slide`、`section`、`deck`、`brand`，表示复用范围。 |
| `transparentPreferred` | 小部件建议 | 是否优先透明背景，便于叠加到不同页面。 |
| `semanticContent` | 小部件必填 | 组件资产必须为 `none`，表示图片不承载文字、编号、方向或业务语义。 |
| `nativePptOwns` | 小部件建议 | PPT 原生元素负责的内容，例如 `label`、`number`、`position`、`direction`。 |

## 组件级资产

不要只列背景图。复杂页面要先拆出可组合的小部件。

```json
{
  "assets": [
    {
      "id": "process-line-blue",
      "kind": "flow-line",
      "path": "assets/imagegen/process-line-blue.png",
      "aspectRatio": "12:1",
      "alt": "Blue luminous process connector line",
      "usage": "timeline connector",
      "componentRole": "line",
      "componentFamily": "blue-process",
      "variant": "default",
      "reuseScope": "deck",
      "transparentPreferred": true,
      "semanticContent": "none",
      "nativePptOwns": ["direction", "length", "position"],
      "minWidth": 1200,
      "minHeight": 80,
      "prompt": "premium blue luminous horizontal connector line, transparent or plain dark background, 12:1, no text, no logo, no arrow"
    },
    {
      "id": "process-node-glass",
      "kind": "flow-node",
      "path": "assets/imagegen/process-node-glass.png",
      "aspectRatio": "1:1",
      "alt": "Glassmorphism circular process node",
      "usage": "process milestone node",
      "componentRole": "node",
      "componentFamily": "blue-process",
      "variant": "default",
      "reuseScope": "deck",
      "transparentPreferred": true,
      "semanticContent": "none",
      "nativePptOwns": ["label", "number", "position"],
      "prompt": "premium glassmorphism circular process node, centered, 1:1, no text, no number, no logo"
    }
  ]
}
```

同一 `componentFamily` 下优先复用默认组件，只为状态差异生成少量变体。
不要把“玻璃质感节点”“蓝色发光线”等视觉描述写进 `semanticContent`；这些内容放在 `alt` 或 `prompt`。

| 组件 | 图片负责 | PPT 原生元素负责 |
| --- | --- | --- |
| `flow-line` | 线条材质、光效、纹理 | 起止点、长度、方向、连接关系 |
| `flow-node` | 节点外观、材质、阴影 | 节点文字、编号、布局位置 |
| `marker` | 状态视觉、强调符号 | 状态含义、标签、说明 |
| `icon-asset` | 风格化位图图标 | 标题、说明、分组关系 |

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

每条图片提示词都要显式包含 `no text`、`no logo`、`no watermark`。只写 `no watermark` 不够。

示例：

| 用途 | 提示词形态 |
| --- | --- |
| 封面 | `premium enterprise cyber operations room, dark negative space on the left, 16:9, no text, no logo` |
| 章节页 | `minimal premium abstract supply-chain data texture, calm center area, 16:9, no text, no logo` |
| 内容页场景图 | `realistic enterprise document automation scene, clean desk, 4:3, no readable text, no logo` |
| 流程线 | `premium luminous horizontal connector line, subtle gradient, 12:1, no text, no arrow, no logo` |
| 流程节点 | `premium circular glass process node, centered, 1:1, no text, no number, no logo` |

## 拒绝规则

出现这些情况时拒绝或重新生成图片：

| 问题 | 原因 |
| --- | --- |
| 比例错误 | 裁切结果不可控。 |
| 有可读假文字 | 会和 PPT 原生文字冲突。 |
| 明显商标或水印 | 有法律和品牌风险。 |
| 安全区细节太多 | 标题对比度容易失败。 |
| 分辨率太低 | 大屏展示会显得粗糙。 |
| 小部件里含文字或箭头语义 | 会削弱 PPT 原生结构的可编辑性。 |
