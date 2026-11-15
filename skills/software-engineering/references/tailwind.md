# Tailwind 可维护模式

在项目已安装 Tailwind 时使用本指南。先确认主版本与仓库现有工具，再实现组件；不要把 v4 规则套用到 v3 项目。

## 目录

- [静态 class 与状态](#静态-class-与状态)
- [重复与组件变体](#重复与组件变体)
- [冲突、任意值与令牌](#冲突任意值与令牌)
- [`@apply` 与 Module](#apply-与-module)
- [响应式与无障碍](#响应式与无障碍)
- [检查清单](#检查清单)
- [依据](#依据)

## 静态 class 与状态

始终让 Tailwind 能在源文件中看到完整 class。把有限状态映射为完整字符串，不插值构造 class 名。

❌ 动态拼接：

```tsx
function Badge({ tone }: { tone: "green" | "red" }) {
  return <span className={`bg-${tone}-500 text-${tone}-950`} />;
}
```

✅ 静态、类型化映射：

```tsx
const toneClasses = {
  green: "bg-green-100 text-green-950",
  red: "bg-red-100 text-red-950",
} satisfies Record<"green" | "red", string>;

function Badge({ tone }: { tone: keyof typeof toneClasses }) {
  return <span className={toneClasses[tone]} />;
}
```

用 Tailwind variant 表达 `hover:`、`focus-visible:`、`disabled:`、`aria-*:`、`data-*:`、`dark:` 和响应式状态。不要用 JS 模拟纯 CSS 状态。

## 重复与组件变体

按以下顺序判断是否抽象：

1. 同一 JSX 由数组循环渲染：没有源代码重复，不抽象 class。
2. 少量重复只存在于一个文件且不会独立演化：允许保留。
3. 跨消费者共享结构、行为与语义契约时考虑组件；仅样式重复时优先已有 class 组合、token 或 variant，不强制提取组件。
4. 同一组件存在有限的 tone、size 或 state：建立静态变体映射。
5. 项目已使用 CVA 或 `tailwind-variants`：沿用现有 helper；否则不要只为一个组件引入依赖。

✅ 简单变体无需新库：

```tsx
const sizeClasses = {
  sm: "h-8 px-3 text-sm",
  md: "h-10 px-4 text-sm",
} as const;
```

组件允许 `className` 时，先明确覆盖契约。优先暴露语义化 props；仅在仓库已有 `twMerge`/`cn` 时用它消解 Tailwind 冲突。不要假设 class 属性中靠后的 utility 一定胜出。

## 冲突、任意值与令牌

- 每个 CSS 属性在同一状态下只保留一个意图明确的 utility。
- 优先使用项目 theme token；任意值只用于真正的一次性、外部品牌值或不可复用的结构计算。
- 同一个任意值第二次出现时，判断是否应提升为主题 token 或语义化 CSS 自定义属性。
- 使用 `@theme` 定义需要生成 utility 的 Tailwind v4 token；使用 `:root` 定义不需要 utility API 的普通变量。
- 沿用项目语义命名，例如 surface、foreground、danger，不在组件中散落新的原始颜色。
- 项目已有 `prettier-plugin-tailwindcss` 时运行它；未安装时不要为单次修改擅自新增。

## `@apply` 与 Module

默认直接在 JSX 使用 utilities。只在以下情况考虑 `@apply`：

- 覆盖只能通过选择器访问的第三方库；
- 一个简单 HTML 元素确需自定义 class，且 React 组件抽象明显过重；
- 现有项目已把该模式作为稳定约定。

Tailwind v4 是完整的 CSS 构建工具，不要把 Sass、Less 或 Stylus 接在同一 Tailwind 处理链上。尤其不要在 `.module.scss` 中通过 `@apply` 重建一套组件类。

在 `.module.css` 中使用 v4 `@apply` 时必须按项目入口使用 `@reference`。若只需要主题值，直接读取 Tailwind 生成的 CSS 变量，避免额外处理：

```css
.root {
  background: var(--color-blue-500);
}
```

如果复杂局部样式需要 Sass，就让 Tailwind 与 `.module.scss` 分工：JSX 中保留常规 utilities，Module 只承担 utilities 不擅长的局部规则。

## 响应式与无障碍

- 从基础样式开始，再添加 `sm:`、`md:` 等增强，保持 mobile-first。
- 交互元素同时覆盖 hover、keyboard focus、disabled 和需要时的 pressed/selected 状态。
- 不用颜色作为唯一状态信号。
- 非必要动画添加 `motion-reduce:` 退化方案；大范围缩放、平移和视差尤其需要处理。
- 自定义表单外观时检查 forced-colors；不要移除焦点轮廓却不给可见替代。
- 面向 RTL 的布局优先使用逻辑方向 utilities，如 `ms-*`、`me-*`、`ps-*`、`pe-*`。

## 检查清单

- [ ] class 都以完整字符串出现在可扫描源码中。
- [ ] 没有互相冲突或重复的 utility。
- [ ] 变体是有限、类型化、语义化的。
- [ ] 重复按样式语义、结构与行为选择已有组合、token、variant 或组件。
- [ ] 任意值没有重复模拟设计令牌。
- [ ] 未把 Tailwind v4 与 SCSS 预处理管线混用。
- [ ] 响应式、focus-visible、disabled、dark 和 reduced-motion 已检查。

## 依据

- [Tailwind：Styling with utility classes](https://tailwindcss.com/docs/styling-with-utility-classes)
- [Tailwind：Detecting classes in source files](https://tailwindcss.com/docs/detecting-classes-in-source-files)
- [Tailwind：Theme variables](https://tailwindcss.com/docs/theme)
- [Tailwind：Functions and directives](https://tailwindcss.com/docs/functions-and-directives)
- [Tailwind：Compatibility](https://tailwindcss.com/docs/compatibility)
- [Tailwind：Automatic class sorting](https://tailwindcss.com/blog/automatic-class-sorting-with-prettier)
- [MDN：prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/%40media/prefers-reduced-motion)
