# 🚀 快速开始指南

> 30分钟搭建你的AI内容系统

---

## 📋 前置要求

### 必需
- Python 3.8+ 或 Node.js 16+
- 目标平台账号（如小红书、抖音等）
- LLM API密钥（Claude/OpenAI/GLM）

### 推荐
- Git
- Docker
- 云服务器（可选）

---

## 🛠️ 第一步：环境准备（5分钟）

### 方式一：本地环境

```bash
# 克隆项目
git clone https://github.com/lobster-journey/ai-creator-starter.git
cd ai-creator-starter

# Python环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Node.js环境
npm install
```

### 方式二：Docker环境

```bash
# 使用Docker Compose
docker-compose up -d
```

---

## 🔑 第二步：配置API密钥（5分钟）

### 创建配置文件

```bash
cp .env.example .env
```

### 编辑.env文件

```bash
# LLM API配置
CLAUDE_API_KEY=your_claude_api_key
OPENAI_API_KEY=your_openai_api_key
GLM_API_KEY=your_glm_api_key

# 图片生成API
DREAMINA_API_KEY=your_dreamina_api_key

# 目标平台Cookie
XIAOHONGSHU_COOKIE=your_cookie
```

---

## 📝 第三步：创建内容模板（10分钟）

### 创建模板文件

```python
# templates/content_template.py

CONTENT_TEMPLATE = """
# {title}

{intro}

## 核心内容

{main_content}

## 总结

{summary}

{hashtags}
"""
```

### 配置内容方向

```python
# config/topics.py

TOPICS = [
    {
        "name": "AI实战技巧",
        "keywords": ["AI", "效率", "工具"],
        "frequency": "每日"
    },
    {
        "name": "科技前沿",
        "keywords": ["新技术", "趋势", "解读"],
        "frequency": "每周3次"
    }
]
```

---

## 🚀 第四步：发布测试（5分钟）

### 测试内容生成

```bash
# 生成测试内容
python tools/content-generator/generate.py --test

# 查看生成结果
cat output/test_content.md
```

### 测试平台发布

```bash
# 发布测试内容（草稿模式）
python tools/publish.py --platform xiaohongshu --draft
```

---

## 📊 第五步：查看数据（5分钟）

### 启动数据看板

```bash
# 启动Web界面
python tools/dashboard.py

# 访问 http://localhost:8080
```

### 查看统计信息

```bash
# 命令行统计
python tools/analytics.py --stats
```

---

## ✅ 验证清单

完成以上步骤后，检查以下项目：

- [ ] 环境配置完成
- [ ] API密钥配置正确
- [ ] 内容模板创建成功
- [ ] 测试内容生成成功
- [ ] 测试发布成功
- [ ] 数据看板正常显示

---

## 🎯 下一步

恭喜！你已经完成了基础搭建。接下来可以：

1. **优化内容模板** - 根据你的领域调整模板
2. **设置定时任务** - 自动化发布流程
3. **配置数据分析** - 建立数据追踪体系
4. **探索高级功能** - 多平台、多账号管理

---

## 📚 相关文档

- [环境配置详解](./environment.md)
- [实施步骤](./steps.md)
- [常见问题](./faq.md)
- [架构设计](./architecture.md)

---

**Created by 🦞 Lobster Journey Studio**
