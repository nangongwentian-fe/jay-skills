# 前端专项路由

保留框架实际约定；React 专项不套用到其他框架。UI 验证需要运行中的页面，服务控制遵循技能入口，不自行启动。

| 问题 | 读取 |
| --- | --- |
| 页面、feature、共享层与数据层归属 | [项目结构](project-structure.md) |
| 组件欠拆、过拆、共享 API 或交互所有权 | [组件边界](component-boundaries.md) |
| 边界取舍的具体例子 | [组件示例](component-examples.md) |
| React 状态、Hook、Effect、身份与服务端边界 | [React 状态与 Hook](react-state-and-hooks.md) |
| 样式维护、复用、区块间距或组件库混排 | [样式组织](styling.md)，含间距失效 bad case；新增布局也须核对 |
| 生成图、背景、照片等静态图片接入或优化 | [图片资产交付](image-assets.md)，含只生成／转格式而未优化尺寸的 bad case |
| Tailwind 扫描、版本与 class 组合 | [Tailwind](tailwind.md) |
| CSS/SCSS Module、Sass 与全局逃逸 | [CSS Modules](css-modules.md) |
| 前端源码 Review | [源码审查](code-review.md) |
| 视觉、键盘、焦点与实际交互 | [UI 审查](ui-review.md) |
| 前端规则来源及取舍 | [来源](sources.md) |

保持 DOM 语义、可访问名称、焦点恢复、组件身份、草稿生命周期和异步过期响应处理。完整前端审查结合代码与页面，合并同根发现；一条验证路径受阻时继续另一条，明确未验证范围。
