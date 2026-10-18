# CSS 与 SCSS Modules 可维护模式

用 Module 承担复杂且局部的样式，不把它当作项目所有 CSS 的收纳箱。文件边界应能从组件边界推导出来。

## 目录

- [文件边界](#文件边界)
- [选择器与命名](#选择器与命名)
- [Sass 模块系统](#sass-模块系统)
- [复用方式](#复用方式)
- [全局逃逸与第三方样式](#全局逃逸与第三方样式)
- [与 Tailwind 共存](#与-tailwind-共存)
- [检查清单](#检查清单)
- [依据](#依据)

## 文件边界

默认让样式与拥有它的组件同目录、同名：

```text
components/
├── dashboard-shell/
│   ├── DashboardShell.tsx
│   └── DashboardShell.module.scss
├── metric-card/
│   ├── MetricCard.tsx
│   └── MetricCard.module.scss
└── activity-list/
    ├── ActivityList.tsx
    └── ActivityList.module.scss
```

一个 Module 可以服务紧密耦合、总是共同演化的内部子组件。出现以下任一信号时拆分：

- 文件包含多个互不相关的顶级区域。
- 样式跨路由或跨独立组件服务。
- 修改一个组件需要理解另一套无关 DOM。
- 文件承担 reset、主题、页面布局和组件细节等多个层级。
- 所谓 shared module 持续增长且消费者只使用其中一小部分。

不要用固定行数机械拆分。拆分后，每个 import 应清楚表达组件对样式的依赖。

## 选择器与命名

- 使用 camelCase、语义化的局部类名，如 `root`、`header`、`emptyState`。
- CSS Modules 已提供局部作用域，不必复制冗长 BEM 命名空间。
- 主要元素使用明确 class，不依赖脆弱的 DOM 层级或标签位置。
- 避免 ID、过高 specificity、`!important` 和宽泛属性选择器。
- 仓库没有更严格 Stylelint 规则时，结构性选择器嵌套最多两层。
- pseudo class、pseudo element 与媒体查询可就近嵌套，但不能借此隐藏更深的结构依赖。

❌ 隐式依赖页面 DOM：

```scss
.dashboard {
  section {
    ul {
      li > button {
        // ...
      }
    }
  }
}
```

✅ 由组件暴露稳定样式接口：

```scss
.activityList {
  // ...
}

.activityItem {
  // ...

  &:focus-within {
    // ...
  }
}
```

## Sass 模块系统

- 使用 `@use` 加载变量、函数和 mixin。
- 使用 `@forward` 为确有多个实现文件的 Sass 工具库提供单一入口。
- 不新增已弃用的 Sass `@import`。
- 保留命名空间，除非仓库已经有清楚且无冲突的 `as *` 约定。
- CSS 自定义属性承担运行期主题；Sass 变量只用于编译期计算或无法由原生 CSS 清楚表达的工具。

```scss
@use "../../styles/mixins" as mixins;

.root {
  @include mixins.truncate(2);
}
```

不要创建只有转发作用却没有多个消费者的 Sass 工具层。

## 复用方式

| 重复类型 | 首选方案 |
| --- | --- |
| 结构与视觉一起重复 | React 组件 |
| 主题值、间距、颜色重复 | CSS 自定义属性或设计令牌 |
| 有参数的 CSS 行为重复 | Sass mixin |
| 同文件单一职责类的层级组合 | CSS Modules `composes` |
| 两个语义类存在真实“是一个”关系 | 受控 `@extend` |
| 单处声明集合 | 保持内联，不抽象 |

`composes` 必须写在其他声明之前，只组合单一局部 class。跨文件组合时保持单向依赖，禁止循环；不要组合会为同一属性提供冲突值的多个来源，因为应用顺序未定义。

```css
.interactive {
  cursor: pointer;
}

.primaryAction {
  composes: interactive;
  color: var(--action-foreground);
}
```

参数化或非语义声明集合优先 mixin。只在语义继承明确、选择器输出可预测时使用 `@extend`；不要为了减少编译后重复文本而承担 cascade 风险。

## 全局逃逸与第三方样式

`:global` 只用于无法控制 class 名的第三方组件或外部生成内容，并在本地根 class 下收窄：

```scss
.editor {
  :global(.third-party-toolbar) {
    border-color: var(--border-muted);
  }
}
```

为非显然的逃逸添加简短原因注释。不要用 `:global(*)`、裸第三方选择器或 Module 中的全局 reset。

## 与 Tailwind 共存

- Tailwind 负责 JSX 中的常规样式，Module 负责复杂局部规则。
- 不把相同属性同时交给 Tailwind 和 Module，以免形成难以预测的覆盖。
- Tailwind v4 不与 Sass 组成同一预处理链；不要在 `.module.scss` 中大量 `@apply`。
- 需要共享 Tailwind 主题值时，优先读取其 CSS 变量。
- 如果项目未安装 Sass 且新增依赖尚未获授权，先说明影响并请求批准；已有授权无需重复确认。否则使用框架已支持的 `.module.css`。

## 检查清单

- [ ] Module 与组件同名、同位置或有明确的组件族边界。
- [ ] 没有跨无关组件的巨型 Module。
- [ ] 局部类使用 camelCase 和低 specificity。
- [ ] 嵌套没有隐藏 DOM 耦合。
- [ ] 使用 `@use`/`@forward`，没有新增 Sass `@import`。
- [ ] 复用方式与重复类型匹配。
- [ ] `composes` 无循环、无跨文件属性冲突。
- [ ] `:global` 狭窄且有理由。
- [ ] Tailwind 与 Module 不重复负责同一属性。

## 依据

- [CSS Modules：README 与局部作用域](https://github.com/css-modules/css-modules)
- [CSS Modules：Composition](https://github.com/css-modules/css-modules/blob/master/docs/composition.md)
- [CSS Modules：Naming](https://github.com/css-modules/css-modules/blob/master/docs/naming.md)
- [Sass：`@import` is deprecated](https://sass-lang.com/blog/import-is-deprecated/)
- [Sass：`@extend`](https://sass-lang.com/documentation/at-rules/extend/)
- [Sass：Style rules and nesting](https://sass-lang.com/documentation/style-rules/)
- [Stylelint：max-nesting-depth](https://stylelint.io/user-guide/rules/max-nesting-depth/)
- [Vite：CSS Modules 与预处理器](https://vite.dev/guide/features.html#css-modules)
