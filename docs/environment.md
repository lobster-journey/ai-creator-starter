# ⚙️ 环境配置详解

> 详细的配置说明和最佳实践

---

## 🖥️ 系统要求

### 最低配置
- CPU: 2核心
- 内存: 4GB
- 存储: 20GB
- 网络: 稳定的互联网连接

### 推荐配置
- CPU: 4核心+
- 内存: 8GB+
- 存储: 50GB+
- 网络: 高速互联网连接

---

## 🐍 Python环境

### 安装Python

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.10 python3-pip

# macOS
brew install python@3.10

# Windows
# 下载安装包：https://www.python.org/downloads/
```

### 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows
```

### 安装依赖

```bash
pip install -r requirements.txt
```

---

## 🟢 Node.js环境

### 安装Node.js

```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs

# macOS
brew install node@18

# Windows
# 下载安装包：https://nodejs.org/
```

### 安装依赖

```bash
npm install
```

---

## 🐳 Docker环境

### 安装Docker

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com | sh

# macOS
brew install --cask docker

# Windows
# 下载Docker Desktop：https://www.docker.com/products/docker-desktop
```

### 使用Docker Compose

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

---

## 🔑 API密钥配置

### LLM API

#### Claude API
```bash
# 获取API密钥
# https://console.anthropic.com/

CLAUDE_API_KEY=sk-ant-api03-xxx
```

#### OpenAI API
```bash
# 获取API密钥
# https://platform.openai.com/api-keys

OPENAI_API_KEY=sk-xxx
```

#### GLM API
```bash
# 获取API密钥
# https://open.bigmodel.cn/

GLM_API_KEY=xxx.xxx
```

---

### 图片生成API

#### 即梦（Dreamina）
```bash
# 获取API密钥
# https://dreamina.baidu.com/

DREAMINA_API_KEY=xxx
```

#### 其他选项
- Midjourney
- DALL-E
- Stable Diffusion

---

### 平台Cookie

#### 小红书Cookie获取

1. 打开Chrome开发者工具（F12）
2. 访问 https://www.xiaohongshu.com
3. 登录你的账号
4. 在开发者工具中找到Cookie
5. 复制完整Cookie字符串

```bash
XIAOHONGSHU_COOKIE=a_session_id=xxx; webId=xxx; ...
```

---

## 📁 目录结构

### 标准结构

```
ai-creator-starter/
├── config/              # 配置文件
│   ├── .env            # 环境变量
│   ├── platforms.json  # 平台配置
│   └── topics.json     # 内容主题配置
│
├── tools/              # 工具脚本
│   ├── content-generator/
│   ├── publisher/
│   └── analytics/
│
├── templates/          # 内容模板
│   ├── article.md
│   └── video.md
│
├── output/             # 输出目录
│   ├── drafts/
│   └── published/
│
├── data/               # 数据目录
│   ├── stats/
│   └── logs/
│
└── docs/               # 文档
```

---

## ⚙️ 配置文件说明

### .env文件

```bash
# LLM API配置
CLAUDE_API_KEY=your_key
OPENAI_API_KEY=your_key
GLM_API_KEY=your_key

# 图片生成API
DREAMINA_API_KEY=your_key

# 平台Cookie
XIAOHONGSHU_COOKIE=your_cookie
DOUYIN_COOKIE=your_cookie

# 数据库配置（可选）
DATABASE_URL=sqlite:///data/creator.db

# 日志级别
LOG_LEVEL=INFO
```

---

### platforms.json

```json
{
  "platforms": [
    {
      "name": "xiaohongshu",
      "enabled": true,
      "publish_time": ["10:00", "14:00", "20:00"],
      "daily_limit": 3
    },
    {
      "name": "douyin",
      "enabled": false,
      "publish_time": ["12:00", "18:00"],
      "daily_limit": 2
    }
  ]
}
```

---

### topics.json

```json
{
  "topics": [
    {
      "name": "AI技巧",
      "keywords": ["AI", "效率", "工具"],
      "frequency": "daily",
      "template": "ai_tips"
    },
    {
      "name": "科技前沿",
      "keywords": ["新技术", "趋势", "解读"],
      "frequency": "weekly",
      "template": "tech_news"
    }
  ]
}
```

---

## 🧪 测试配置

### 测试API连接

```bash
# 测试LLM API
python tools/test_api.py --claude
python tools/test_api.py --openai

# 测试平台连接
python tools/test_platform.py --xiaohongshu
```

### 测试发布流程

```bash
# 发布测试内容（草稿模式）
python tools/publish.py --test --draft
```

---

## 🔧 常见问题

### API密钥无效
- 检查密钥格式
- 确认账户余额
- 检查API限流

### Cookie过期
- 定期更新Cookie
- 使用刷新令牌
- 监控登录状态

### 环境变量不生效
- 确认.env文件位置
- 重启服务
- 检查文件权限

---

## 📚 相关文档

- [快速开始](./quick-start.md)
- [架构设计](./architecture.md)
- [常见问题](./faq.md)

---

**Created by 🦞 Lobster Journey Studio**
