# 文档阅读与进化 - 使用指南

## 快速开始

### 阅读微信公众号文章

```bash
python3 ~/.openclaw/skills/document-evolution/scripts/evolve.py \
  "https://mp.weixin.qq.com/s/xxx" \
  --type wechat
```

### 阅读网页文章

```bash
python3 ~/.openclaw/skills/document-evolution/scripts/evolve.py \
  "https://example.com/article" \
  --type web
```

---

## 完整流程

### 1. 阅读文档

**微信公众号文章**：
```bash
cd ~/.openclaw/skills/wechat-article-to-markdown
node index.js "https://mp.weixin.qq.com/s/xxx"
```

**网页文章**：
```bash
# 使用OpenClaw的web_fetch工具
web_fetch --url "https://example.com/article"
```

### 2. 总结文档

```bash
# 使用tldr工具
# 通过OpenClaw调用tldr skill
```

### 3. 分析业务影响

**分析维度**：
- 对业务的帮助
- 可借鉴的经验
- 优化建议
- 实施路径

### 4. 分析技术影响

**分析维度**：
- 技术架构优化
- 代码模式改进
- 工具链升级

### 5. 代码修改（如需）

**重要原则**：
- ✅ 先分析，再设计，最后实现
- ✅ 编写测试用例
- ✅ 本地测试通过
- ✅ 验证功能正常
- ✅ 更新相关文档
- ✅ 提交到Git

**测试验证流程**：
```bash
# 1. 修改代码
vim path/to/file.py

# 2. 编写测试
vim tests/test_file.py

# 3. 运行测试
pytest tests/test_file.py -v

# 4. 验证功能
python3 -m path/to/file.py

# 5. 提交代码
git add .
git commit -m "feat: 优化xxx"
git push
```

---

## 输出格式

### 分析报告

报告保存在：`~/.openclaw/workspace/document_evolution/report_YYYYMMDD_HHMMSS.md`

**报告结构**：
1. 文档总结
2. 业务分析
3. 技术分析
4. 实施计划

---

## 示例

### 案例：阅读OpenClaw文档

```bash
# 1. 阅读文档
python3 ~/.openclaw/skills/document-evolution/scripts/evolve.py \
  "https://docs.openclaw.ai/xxx" \
  --type web

# 2. 总结文档
# 使用tldr skill

# 3. 分析业务和技术影响
# 手动分析或使用AI工具

# 4. 如需修改代码
# 按照测试验证流程执行
```

---

## 注意事项

### ⚠️ 代码修改规则

**必须**：
1. ✅ 先分析，再设计，最后实现
2. ✅ 编写测试用例
3. ✅ 本地测试通过
4. ✅ 验证功能正常
5. ✅ 更新相关文档
6. ✅ 提交到Git

**禁止**：
- ❌ 直接修改代码不测试
- ❌ 跳过测试用例
- ❌ 不验证就提交

---

## 工具依赖

### 必需工具
- Python 3.x
- Node.js
- pytest（测试框架）

### OpenClaw工具
- web_fetch
- tldr
- wechat-article-to-markdown

---

## 更新日志

**v1.0.0** (2026-04-20)
- ✅ 创建skill
- ✅ 实现基础功能
- ✅ 编写使用指南

---

*Created by 🦞 Lobster Journey Studio*
