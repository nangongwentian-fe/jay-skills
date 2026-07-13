---
name: web-content-fetcher
description: 获取公开网页的正文或 Markdown 内容。当用户要求抓取链接、读取文章、提取网页正文、将页面转为 Markdown，或获取 X/Twitter、微信、知乎、Medium 等公开页面的文字内容时使用。支持在直接抓取失败或内容不完整时，通过内容提取代理和网页搜索逐级回退；不适用于需要登录的页面、付费墙绕过、媒体下载或结构化数据抓取。
---

# 网页内容获取技巧集合

本 skill 的核心思路：**渐进回退，确保拿到内容。**

## 回退策略

任何 URL 都按以下顺序尝试，不区分网页类型：

1. **WebFetch 直接抓取** — 最快，先试
2. **如果失败或内容不完整** — 并行尝试 `r.jina.ai` 和 `defuddle.md` 两种代理前缀，取内容更完整的结果
3. **如果代理也失败** — 使用 WebSearch 搜索相关内容作为兜底

"不完整"的判断：返回正文少于 200 字、明显缺失关键段落、或返回错误/空白页面。

---

## 方法一：r.jina.ai 前缀

在目标 URL 前加上 `https://r.jina.ai/` 前缀，用 WebFetch 抓取：

```
https://r.jina.ai/<目标URL>
```

**示例**

```
https://r.jina.ai/https://x.com/qoder_ai_ide/status/2036437931867644016
https://r.jina.ai/https://www.anthropic.com/engineering/some-post
https://r.jina.ai/https://any-website.com/any-page
```

**特点**

- 会自动执行 JS 渲染，对动态页面和 SPA 支持好
- 返回经过清洗的 Markdown 格式正文
- 响应稍慢但内容覆盖面广

---

## 方法二：defuddle.md 前缀

在目标 URL 前加上 `https://defuddle.md/` 前缀，用 WebFetch 抓取：

```
https://defuddle.md/<目标URL>
```

**示例**

```
https://defuddle.md/https://mp.weixin.qq.com/s/ERSjcq9YURHvlsdTUv_Paw
https://defuddle.md/https://example.com/some-article
https://defuddle.md/https://any-website.com/any-page
```

**特点**

- 自动去除广告、导航栏等干扰元素，只保留正文
- 返回 Markdown 格式
- 响应较快

---

## 通用注意事项

- 两种代理方式都仅支持公开可访问的页面，需要登录的内容无法获取
- 图片等媒体资源不会返回，仅返回文字内容
- 两种方式各有擅长，无法预知哪个对特定网站效果更好，所以失败时应并行尝试两者

---

> 本 skill 持续更新中。如需添加新的获取方法，按照相同格式补充即可。
