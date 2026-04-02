# 飞书富文本元素使用指南

## 目录
1. [Callout 高亮块](#callout)
2. [Grid 分栏](#grid)
3. [lark-table 增强表格](#lark-table)
4. [文字染色](#文字染色)
5. [画板](#画板)
6. [组合模式](#组合模式)
7. [反例：这样写就是朴素](#反例)

---

## Callout 高亮块 {#callout}

### 语法
```html
<callout emoji="💡" background-color="light-blue">
内容（支持**加粗**、列表、标题）
</callout>
```

### 颜色速查表
| emoji | background-color | 使用场景 |
|-------|-----------------|---------|
| 💡 | light-blue | 提示、说明、背景介绍 |
| ⚠️ | light-yellow | 警告、注意事项、风险 |
| ❌ | light-red | 危险操作、错误示例、禁止项 |
| ✅ | light-green | 成功、结论、推荐做法 |
| 📌 | pale-gray | 备注、补充说明、参考资料 |
| 🎯 | light-orange | 目标、重点、核心结论 |
| 🔍 | light-purple | 探索、研究、调查发现 |

### 限制
- 内部不支持：代码块、表格、图片
- 内部支持：文本、标题(h1-h6)、列表、待办、引用

---

## Grid 分栏 {#grid}

### 语法
```html
<grid cols="2">
<column>

左栏内容（前后必须空行）

</column>
<column>

右栏内容

</column>
</grid>
```

### 使用场景
- ✅ 传统 vs 新方式对比
- ✅ 优点 vs 缺点
- ✅ 方案A vs 方案B
- ✅ 两个并排的 callout（踩坑记录、注意事项）
- ✅ 左说明右示例

### 自定义列宽（三栏示例）
```html
<grid cols="3">
<column width="20">20%</column>
<column width="60">60%（主内容）</column>
<column width="20">20%</column>
</grid>
```

---

## lark-table 增强表格 {#lark-table}

**只在单元格需要富文本（代码、列表、callout）时使用，否则用 Markdown 表格。**

### 语法
```html
<lark-table column-widths="200,250,280" header-row="true">
<lark-tr>
<lark-td>

**表头1**

</lark-td>
<lark-td>

**表头2**

</lark-td>
</lark-tr>
<lark-tr>
<lark-td>

普通文本

</lark-td>
<lark-td>

- 列表项1
- 列表项2

</lark-td>
</lark-tr>
</lark-table>
```

**关键规则：`<lark-td>` 内容前后必须有空行**

### 列宽参考（总宽约 730px）
| 场景 | 建议列宽 |
|------|---------|
| 2列等宽 | `365,365` |
| 3列等宽 | `240,240,250` |
| 名称+说明 | `200,530` |
| 工具+类型+描述 | `220,150,360` |

---

## 文字染色 {#文字染色}

### 行内文字颜色
```html
<text color="blue">蓝色关键词</text>
<text color="red">红色警告词</text>
<text color="green">绿色成功词</text>
<text color="orange">橙色提示词</text>
<text color="purple">紫色特殊词</text>
<text color="gray">灰色次要词</text>
```

### 行内背景高亮
```html
<text background-color="yellow">黄色高亮</text>
<text background-color="light-blue">蓝色高亮</text>
```

### 彩色标题
```markdown
## 重要章节 {color="blue"}
### 警告区域 {color="red"}
```

### 使用原则
- 全文不超过 3 种颜色
- 同一颜色含义要统一（蓝=工具名，红=警告，绿=成功）
- 不要给普通正文文字染色，只给关键词/术语

---

## 画板 {#画板}

### 创建空白画板
```html
<whiteboard type="blank"></whiteboard>
```

### 使用场景
- 复杂架构图（节点超过5个）
- 流程图（分支超过3条）
- 手绘草图、UI 线框图
- 思维导图

### 简单流程的替代方案（不用画板）
```
Step 1: 输入 → Step 2: 处理 → Step 3: 输出
```
或用有序列表 + 缩进表示层次关系。

---

## 组合模式 {#组合模式}

### 模式1：对比型章节
```html
<grid cols="2">
<column>

<callout emoji="❌" background-color="light-red">
**旧方式问题**
- 问题1
- 问题2
</callout>

</column>
<column>

<callout emoji="✅" background-color="light-green">
**新方式优势**
- 优势1
- 优势2
</callout>

</column>
</grid>
```

### 模式2：工具/选项列表
```html
<lark-table column-widths="200,130,400" header-row="true">
<lark-tr>
<lark-td>**工具名**</lark-td>
<lark-td>**安装量**</lark-td>
<lark-td>**说明**</lark-td>
</lark-tr>
<!-- 每个工具一行，说明列可含代码块 -->
</lark-table>
```

### 模式3：步骤 + 代码
```markdown
1. **步骤一：安装依赖**

   ```bash
   npm install xxx
   ```

2. **步骤二：配置**

   修改 `config.json`：
   ```json
   { "key": "value" }
   ```
```

### 模式4：踩坑记录
```html
<grid cols="2">
<column>

<callout emoji="❌" background-color="light-red">
**坑1：字体写法**
`"SemiBold"` → 错误
`"Semi Bold"` → 正确
</callout>

</column>
<column>

<callout emoji="❌" background-color="light-red">
**坑2：页面切换**
`figma.currentPage = p` → 错误
`await figma.setCurrentPageAsync(p)` → 正确
</callout>

</column>
</grid>
```

---

## 反例：这样写就是朴素 {#反例}

❌ **纯文字列表堆砌**
```
工具1：用于做A
工具2：用于做B
工具3：用于做C
```
→ 改用 lark-table

❌ **重要信息埋在段落中**
```
注意：在使用前必须安装桌面应用，否则无法连接。
```
→ 改用 callout

❌ **对比用文字描述**
```
传统方式需要手动操作，而新方式可以自动化。传统方式...
```
→ 改用 grid 分栏

❌ **步骤没有代码块**
```
运行 npm install 安装依赖，然后运行 npm run dev 启动。
```
→ 步骤必须配代码块
