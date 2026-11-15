# 组件拆分正反示例

这些示例用于校准判断，不是必须复制的目录模板。

## Contents

- [保持内联](#保持内联)
- [提取私有语义组件](#提取私有语义组件)
- [提取逻辑而不新增 DOM](#提取逻辑而不新增-dom)
- [建立业务共享组件](#建立业务共享组件)
- [避免视觉驱动的通用卡片](#避免视觉驱动的通用卡片)
- [避免强制容器与展示组件二分](#避免强制容器与展示组件二分)
- [避免 Props 配置爆炸](#避免-props-配置爆炸)
- [Review Output](#review-output)

## 保持内联

✅ 一次性、短小且只服务当前语境：

```tsx
function AccountHeader({ user }: Props) {
  return (
    <header>
      <h1>{user.name}</h1>
      {user.isTrial ? <span>Trial</span> : null}
    </header>
  );
}
```

`TrialBadge` 没有独立行为、变化原因或真实复用时，提取只会增加跳转成本。

## 提取私有语义组件

✅ 一个页面区域拥有完整状态和交互，但没有跨页面复用：

```tsx
export function CheckoutPage() {
  return (
    <CheckoutLayout>
      <DeliveryAddressSection />
      <PaymentMethodSection />
      <OrderReviewSection />
    </CheckoutLayout>
  );
}
```

这些组件可以与页面共置并保持私有。它们的价值来自独立业务语义和变化原因，不依赖共享层复用。

## 提取逻辑而不新增 DOM

✅ 请求、取消、错误和重试构成可命名逻辑：

```tsx
function SearchResults({ query }: { query: string }) {
  const result = useProductSearch(query);

  if (result.status === "error") {
    return <SearchError onRetry={result.retry} />;
  }

  return <ProductResults items={result.items} loading={result.status === "loading"} />;
}
```

Hook 负责搜索生命周期，组件继续拥有用户可见状态组合。不要把标题、布局和卡片 JSX 一并塞入 Hook。

## 建立业务共享组件

✅ 两个真实消费者共享同一领域对象、动作和语义：

```tsx
<CategoryCard category={category} onSelect={handleSelect} />
```

当首页和分类页都把它理解为“选择分类”的完整卡片时，可以共享。路由差异由领域事件 `onSelect` 注入。

## 避免视觉驱动的通用卡片

❌ 不相关业务只因圆角、阴影相似就合并：

```tsx
<UniversalCard
  clickable
  compact={false}
  entity={supplier}
  showStatus
  showThumbnail
  variant="supplier"
/>
```

✅ 保留 `SupplierCard` 与 `CategoryCard` 的业务 API；真正稳定的阴影、边框或间距由 token、样式配方或基础容器承担。

## 避免强制容器与展示组件二分

❌ 每个组件都增加无行为的包装层：

```tsx
function ProfileContainer() {
  const profile = useProfile();
  return <ProfileView {...profile} />;
}
```

当 `ProfileContainer` 没有独立组合、路由或错误边界价值时，直接在 `Profile` 中调用专用 Hook 更清楚。若同一视图确实需要多个数据源或隔离渲染契约，容器模式仍可使用。

## 避免 Props 配置爆炸

❌ 用布尔开关模拟多个不同组件：

```tsx
<Panel
  collapsible
  hasSearch
  showFooter={false}
  stickyHeader
  useCompactRows
/>
```

✅ 用组合表达结构，用明确组件表达稳定变体：

```tsx
<SearchablePanel header={<CatalogHeader />}>
  <CompactProductRows products={products} />
</SearchablePanel>
```

如果组合后仍需要大量内部条件，说明这些场景可能不共享同一个语义契约。

## Review Output

评审时按优先级输出：

1. 说明当前边界是否影响正确性、状态身份、可访问性或维护性。
2. 指出具体职责和变化原因，不以“文件太长”作为唯一理由。
3. 选择保持、私有提取、逻辑提取、业务共享或基础组件之一。
4. 说明应保持的 props、DOM、状态和行为。
5. 给出与风险相称的验证场景。

没有足够拆分信号时，明确建议保持现状，避免制造工作。
