# 命令参考

## 初始化

```bash
mkdir -p ~/.persistent-memory/memory
```

## 会话开始

```bash
# 读取长期记忆
cat ~/.persistent-memory/MEMORY.md

# 读取今日
cat ~/.persistent-memory/memory/$(date +%Y-%m-%d).md

# 读取昨日
cat ~/.persistent-memory/memory/$(date -d "yesterday" +%Y-%m-%d).md
```

## 记住信息

```bash
# 追加到长期记忆
echo "- 2026-02-28: 新记录" >> ~/.persistent-memory/MEMORY.md

# 追加到今日日记
echo "### 今日" >> ~/.persistent-memory/memory/$(date +%Y-%m-%d).md
echo "- 完成了 Agent Reach 安装" >> ~/.persistent-memory/memory/$(date +%Y-%m-%d).md
```

## 搜索

```bash
# 文本搜索
grep -ri "关键词" ~/.persistent-memory/

# 查看最近日记
ls -t ~/.persistent-memory/memory/ | head -7
```

## 备份

```bash
# 打包备份
tar -czf memory-backup.tar.gz ~/.persistent-memory/

# 导出为文本
cat ~/.persistent-memory/MEMORY.md > memory.txt
```

## 敏感信息检测

```bash
grep -E "(sk-|ghp_|eyJh|bearer|password|secret)" ~/.persistent-memory/ -r
```
