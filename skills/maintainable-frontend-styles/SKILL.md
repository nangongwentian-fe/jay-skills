---
name: maintainable-frontend-styles
description: "Implement or refactor component styles using the project's Tailwind and CSS/SCSS conventions. Use for style boundaries, reuse, variants and maintainability."
---

# Maintainable Frontend Styles

沿用仓库的样式方案。已有 Tailwind 时用完整、可静态检测的 utility class 表达常规样式；复杂局部规则可放在组件同位置的 CSS/SCSS Module。

## 选择最小充分方案

| 需求 | 方案 |
| --- | --- |
| 布局、间距、排版、主题与常规交互状态 | 项目现有 utility、token 和 variant |
| 复杂选择器、伪元素、关键帧或局部第三方覆盖 | 组件 CSS/SCSS Module |
| reset、字体、主题令牌及真正的全局基础样式 | 全局样式入口 |
| 不能静态枚举的运行时值 | 局部 CSS 自定义属性，必要时 inline style |

明确的项目规则优先于本表，不为遵循个人默认方案而迁移技术栈。常规局部实现可自主完成；新增依赖、构建机制或扩大迁移范围超出既有授权时，先说明具体变更并确认，已有授权不重复询问。

只读取当前组件和决定本次改动的项目事实。涉及工具语法时确认实际版本；涉及构建、全局入口或样式复用时再检查对应配置和调用方。

## 复用与边界

- 不为了减少 class 字符数切换方案，不动态拼接有限状态的 Tailwind class。
- 循环可消除同一上下文的重复；跨消费者共享结构和行为时考虑组件；同一组件的样式差异用现有 variant 机制。
- 不因一次重复新增依赖或共享抽象，也不把不同组件的局部规则集中成巨型样式文件。
- 保持样式作用域、可访问性和未要求改变的视觉行为，不顺手重构相邻代码。

## 按需参考

- Tailwind 版本差异、class 合并或变体设计：[tailwind-patterns.md](references/tailwind-patterns.md)。
- Module 作用域、Sass 复用或大型样式文件拆分：[scss-modules-patterns.md](references/scss-modules-patterns.md)。
- 样式架构评审、迁移或存在交互/视觉回归风险：[review-playbook.md](references/review-playbook.md)。

已明确的简单 token 或 class 调整无需预读全部参考。

## 验证与交付

选择能覆盖受影响行为的检查：局部样式调整检查实际视觉结果及相关断点/状态；改动 props 或逻辑时做相关类型与行为验证；涉及构建、入口或 CSS 顺序时再执行生产构建。保留项目强制门禁。

修复本次改动引入的缺陷，按任务规则清理验证资源，交付实际验证结果及有意义的未验证项。不要每次运行全部 formatter、lint、测试、构建及所有主题状态，也不要为通过检查改写无关文件。
