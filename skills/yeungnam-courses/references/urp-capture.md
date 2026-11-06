# URP 页面与虚拟表格采集

以下定位来自2026年11月5日的实际页面，用于减少重复摸索。先从当前页面状态确认元素存在且含义一致；页面改版后重新定位，不机械套用 ID、列位置或旧结果。浏览器 API 以当前运行时返回的文档为准。

## 页面定位起点

| 用途 | 曾验证的元素 ID／控件 |
| --- | --- |
| 年份输入 | `mf_tac_layout_contents_W010202_body_inSearchYy` |
| 学期原生 select | `mf_tac_layout_contents_W010202_body_sbSearchShtmCd_input_0` |
| 学院原生 select | `mf_tac_layout_contents_W010202_body_sbSearchUnivCd_input_0` |
| 学部原生 select | `mf_tac_layout_contents_W010202_body_sbSearchSustCd_input_0` |
| 专业自定义下拉 | `mf_tac_layout_contents_W010202_body_sbSearchMjCd` |
| 年级原生 select | `mf_tac_layout_contents_W010202_body_sbSearchShyrCd_input_0` |
| 查询 | 显示名精确为 `조회` 的链接 |
| 课程表 | `mf_tac_layout_contents_W010202_body_gdTmLsn_body_table` |
| 表格可视层 | `mf_tac_layout_contents_W010202_body_gdTmLsn_dataLayer` |
| 垂直滚动条 | `mf_tac_layout_contents_W010202_body_gdTmLsn_scrollY_div` |
| 结果计数 | `mf_tac_layout_contents_W010202_body_gdTmLsn_rowCount` |

专业下拉曾以弹出表格中的 `listitem` 呈现，不能假定它是原生 `select`。先打开下拉、读取选项，再点击精确的专业名。不要复用旧快照里的数字元素索引。

年份、学期或学院变化会触发异步更新。一次点击成功不代表下级选项已更新；目标年度的学院、专业列表也可能变化。以新的选项和所选条件为准。固定长时间等待会拖慢流程，应使用当前工具支持的加载／控件状态检查。

## 只读提取可见行

若浏览器运行时允许只读 DOM evaluation，可在**当前页面已经确认上述表格和可视层**后按下面思路提取一屏。这是数据读取片段，不包含连接浏览器、点击或滚动；将其放入当前运行时已文档化的只读页面求值接口。

```js
() => {
  const table = document.getElementById(
    'mf_tac_layout_contents_W010202_body_gdTmLsn_body_table');
  const layer = document.getElementById(
    'mf_tac_layout_contents_W010202_body_gdTmLsn_dataLayer');
  if (!table || !layer) throw new Error('需要重新定位课程表');
  const box = layer.getBoundingClientRect();
  return [...table.querySelectorAll('tbody tr')]
    .filter(row => {
      const r = row.getBoundingClientRect();
      return r.height > 0 && r.top >= box.top &&
        r.bottom <= Math.min(box.bottom, window.innerHeight);
    })
    .map(row => [...row.children].map(cell => cell.innerText));
}
```

读取前确认表格未被加载遮罩或弹窗覆盖。正高度和区域相交不能单独证明内容已稳定；应结合当前加载状态、可见页面和重叠行检查。DOM能力不可用时，依据可见表格或页面提供的导出操作完成采集，不绕过浏览器连接限制。

### 字段映射

先读当前表头及每行单元格结构，确认列数和字段归属后映射，不对数据行做“过滤空白单元格”，否则会错列。2026年的页面曾包含42个逻辑列，部分为隐藏元数据；常用字段当时的0基索引如下，仅作核对线索：

| 索引 | 字段 | 索引 | 字段 |
| --- | --- | --- | --- |
| 0 | 년도 学年 | 2 | 학년 年级 |
| 3 | 이수구분 课程类别 | 4 | 수강번호 选课编号 |
| 5 | 교과목명 课程名 | 6 | 과목유형 课程类型 |
| 10 | 담당교수 教师 | 11 | 반 班级 |
| 12 | 강의시간 时间 | 13 | 강의실 教室 |
| 14 | 학점 学分 | 32 | 비고 备注 |
| 35 | 개설학과 开课专业 | 39 | haksuNo 学修编号 |

当时表头中的学期列在数据行为空，学期应从本次已确认的筛选条件取得；索引2是**年级**，不是学期。学修编号（haksuNo）也不等于选课编号（수강번호）。

页面隐藏行曾出现编号和课程正确、教师或班级却残留旧值的情况。只检查“编号存在”或“年份非空”不能排除这类混合行；必须排除未渲染行并核对重叠行。滚动到尾部仍不够，最终需要与页面计数对齐。

## 真实案例的适用边界

2026年11月5日，以计算机工学专业、全部年级查询2026—2028年：2026年第1学期34条、夏季2条、第2学期37条；2026冬季和2027年第1学期查询为0条，其余组合提示年度学期无法查询。它只说明当次状态区分和采集方法，不是未来执行的预期数量或当前开课事实。不要将这些数量、年份范围写成筛选默认值或通过条件。

发布前或修改采集逻辑时可用以下情境复核判断：

- 第一屏12行、计数37：继续滚动并保留重叠，不能只导出12行。
- 隐藏行有编号但高度为0：不采集，即使看起来字段齐全。
- 切换学期后旧表仍显示37：等待本次查询完成，不能把旧行标成新学期。
- 两个不同选课编号对应同一课程名：保留两个班次。
- 系统提示年度学期无法查询：记录不可查询和空数量，不写0，不用历史班次补齐。
