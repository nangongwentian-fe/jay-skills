# 来源与取舍

核对日期：2026-11-07。以下是上游参考入口，不是锁定依赖版本；引用特定 API 时另核对目标项目版本。参考原则经过适用范围筛选，不能把参考项目所有代码都视作规范。

- [Bulletproof React](https://github.com/alan2207/bulletproof-react)：主要工程参考，属于有观点的指南与示例应用，并非所有规模的统一模板。
- [Project structure](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-structure.md)：借鉴业务内聚、按需建目录和依赖方向；跨 feature 禁止导入及 barrel 取舍保留为项目策略。
- [Components and styling](https://github.com/alan2207/bulletproof-react/blob/master/docs/components-and-styling.md)：借鉴就近放置、职责拆分和组合；不将包装所有第三方组件或 props 数量上限变成要求。
- [State management](https://github.com/alan2207/bulletproof-react/blob/master/docs/state-management.md)：参考状态分类；不绑定它列出的具体状态库或表单库。
- [业务查询示例](https://github.com/alan2207/bulletproof-react/blob/master/apps/react-vite/src/features/discussions/api/get-discussions.ts)：用于说明职责分离与同文件组织可以并存，不复制代码作为通用实现。
- [React 自定义 Hook](https://react.dev/learn/reusing-logic-with-custom-hooks)：Hook 提取、命名及独立状态语义。
- [React Effect 取舍](https://react.dev/learn/you-might-not-need-an-effect)：派生值、事件处理和外部同步的区别。
- [React 状态保留与重置](https://react.dev/learn/preserving-and-resetting-state)：组件身份、树位置及 key 的状态语义。

- [Next.js 服务端与客户端组件](https://nextjs.org/docs/app/getting-started/server-and-client-components)：边界示例；实际使用前核对目标框架与版本，不将 Next.js 约定视为所有 React 应用的要求。

这些链接用于溯源和有疑问时核实，不要求每次实施联网重读。Cal.com 等大型产品可在研究特定复杂模块时补充证据；本技能不据此预设 monorepo 分层、框架或产品规模。
