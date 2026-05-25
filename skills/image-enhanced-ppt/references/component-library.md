# 组件库规则

组件库的目标是让 Agent 组装 PPT，而不是每页重新画一张图。

```text
PPT = 版式系统 + PPT 原生结构元素 + 图片组件库
```

## 决策顺序

| 顺序 | 判断 | 动作 |
| --- | --- | --- |
| 1 | 已有组件可直接使用 | 复用原组件。 |
| 2 | 已有组件风格正确但状态不同 | 基于同一 `componentFamily` 生成 `variant`。 |
| 3 | 组件库缺少该角色 | 生成新组件，并登记字段。 |
| 4 | Agent 想生成背景图代替结构 | 拒绝，先拆成线、点、图标、文本。 |
| 5 | Agent 想生成整页图 | 拒绝，除非用户明确要求不可编辑海报页。 |

## 组件字段

```json
{
  "id": "process-node-glass-active",
  "kind": "flow-node",
  "componentRole": "node",
  "componentFamily": "blue-process",
  "variant": "active",
  "reuseScope": "deck",
  "transparentPreferred": true,
  "semanticContent": "none",
  "nativePptOwns": ["label", "number", "position"],
  "aspectRatio": "1:1",
  "path": "assets/imagegen/process-node-glass-active.png",
  "prompt": "premium glass circular process node, active blue glow, 1:1, no text, no number, no logo"
}
```

| 字段 | 作用 |
| --- | --- |
| `componentRole` | 说明组件在页面中扮演什么角色。 |
| `componentFamily` | 把同一视觉系统的组件归到一组。 |
| `variant` | 表示状态或样式差异。 |
| `reuseScope` | 说明复用范围：`slide`、`section`、`deck`、`brand`。 |
| `transparentPreferred` | 小部件优先透明背景，便于叠加。 |
| `semanticContent` | 组件资产必须为 `none`，避免图片承载语义。 |
| `nativePptOwns` | 标明哪些内容必须由 PPT 原生元素控制。 |

视觉描述写进 `alt` 或 `prompt`。不要把“发光线”“玻璃节点”“警告标记”等描述写进 `semanticContent`。

## 组件族

| 组件族 | 建议包含 |
| --- | --- |
| 流程组件族 | `flow-line.default`、`flow-node.default`、`flow-node.active`、`marker.warning` |
| 时间线组件族 | `flow-line.default`、`marker.default`、`marker.active` |
| 架构组件族 | `icon-asset.service`、`icon-asset.database`、`marker.risk` |
| 指标卡组件族 | `texture.card-bg`、`marker.up`、`marker.down` |

同一组件族要共享材质、光线、线宽、圆角和阴影规则。

## 复用检查

| 问题 | 判断方式 | 改法 |
| --- | --- | --- |
| 每页都有相似节点 | 多个 `flow-node` 只有轻微颜色差异 | 合并成一个组件族，用 `variant` 管理状态。 |
| 背景图承载流程图 | 背景图里画了线、点、文字 | 拆成 `flow-line`、`flow-node` 和原生文本。 |
| 图标风格不一致 | 每页图标材质、角度、光线不同 | 建立 `icon-asset` 组件族。 |
| 小部件不能叠加 | 图片有脏底色或大块背景 | 重新生成透明背景或纯净底色版本。 |

## 语义边界

| 图片组件可以做 | PPT 原生元素必须做 |
| --- | --- |
| 材质、纹理、光效、阴影、外观 | 文本、编号、箭头方向、连接关系 |
| 节点外壳、状态色、图标外观 | 节点含义、状态标签、数据值 |
| 分隔线皮肤、连接线皮肤 | 起点、终点、长度、对齐 |

## 页面拆分例子

| 页面 | 图片组件 | PPT 原生元素 |
| --- | --- | --- |
| 三步流程 | `flow-line.default`、`flow-node.default`、`flow-node.active` | 步骤标题、说明、编号、连接位置 |
| 风险时间线 | `flow-line.default`、`marker.warning`、`marker.resolved` | 日期、风险说明、状态文字 |
| 系统架构 | `icon-asset.service`、`icon-asset.database`、`marker.risk` | 容器、连线、模块名、依赖关系 |

## 生成提示

组件提示词要强调“单个组件”，不要让图片模型生成完整页面。
每条组件提示词都要显式包含 `no text`、`no logo`、`no watermark`。

| 组件 | 提示词要点 |
| --- | --- |
| 流程线 | `single horizontal connector line, 12:1, no arrow, no text, no logo, no watermark, transparent background` |
| 流程节点 | `single circular process node, centered, 1:1, no number, no text, no logo, no watermark, transparent background` |
| 状态标记 | `single warning marker badge, centered, 1:1, no text, no logo, no watermark, transparent background` |
| 图标 | `single enterprise automation icon, centered, 1:1, no label, no text, no logo, no watermark, transparent background` |
