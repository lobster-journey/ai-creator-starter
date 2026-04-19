# 🔧 环境配置

## 📋 配置清单

在开始之前，你需要准备以下内容：

### 必需配置
1. ✅ LLM API（Claude/GPT/GLM）
2. ✅ 平台账号（小红书等）
3. ✅ OpenClaw环境

### 可选配置
4. ⭕ 图像生成API
5. ⭕ 数据库

---

## 1️⃣ 配置LLM API

### 获取API密钥

你需要选择一个LLM服务并获取API密钥：

#### Claude (Anthropic)

**注册步骤**：
1. 访问官网：https://console.anthropic.com
2. 注册账号（需要国外手机号或邮箱）
3. 登录后点击「API Keys」
4. 点击「Create Key」生成密钥
5. 新用户有免费额度

**配置方式**：
```bash
# 编辑配置文件
vim ~/.openclaw/workspace/config/.env

# 添加以下内容
ANTHROPIC_API_KEY=your-api-key-here
```

#### OpenAI (GPT)

**注册步骤**：
1. 访问官网：https://platform.openai.com
2. 注册账号（需要国外手机号）
3. 登录后点击「API Keys」
4. 点击「Create new secret key」
5. 需要绑定信用卡

**配置方式**：
```bash
# 编辑配置文件
vim ~/.openclaw/workspace/config/.env

# 添加以下内容
OPENAI_API_KEY=your-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
```

#### 智谱AI (GLM)

**注册步骤**：
1. 访问官网：https://open.bigmodel.cn
2. 注册账号（国内手机号即可）
3. 登录后点击「API密钥」
4. 点击「创建密钥」
5. 新用户有免费额度

**配置方式**：
```bash
# 编辑配置文件
vim ~/.openclaw/workspace/config/.env

# 添加以下内容
GLM_API_KEY=your-api-key-here
GLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4
```

### 方式二：使用OneAPI（统一接口）

**优点**：
- 统一接口调用多个模型
- 成本可控
- 国内可用

**注册步骤**：
1. 访问OneAPI平台
2. 注册账号
3. 充值余额
4. 获取API Key

**配置方式**：
```bash
# 编辑配置文件
vim ~/.openclaw/workspace/config/.env

# 添加以下内容
ONEAPI_API_KEY=your-api-key-here
ONEAPI_BASE_URL=https://api.oneapi.com/v1
```

### 测试API

配置完成后，测试API是否可用：

```bash
# 测试Claude API
curl -X POST https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-3-sonnet-20240229",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello"}]
  }'

# 测试OpenAI API
curl -X POST https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Hello"}]
  }'

# 测试GLM API
curl -X POST https://open.bigmodel.cn/api/paas/v4/chat/completions \
  -H "Authorization: Bearer $GLM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "glm-4",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

---

## 2️⃣ 配置平台账号

### 小红书配置

**步骤**：

1. **登录小红书创作者平台**
   - 访问：https://creator.xiaohongshu.com
   - 使用手机扫码登录

2. **导出Cookie**
   - 打开浏览器开发者工具（F12）
   - 切换到Application/存储标签
   - 找到Cookies → https://creator.xiaohongshu.com
   - 复制所有Cookie信息

3. **保存Cookie**
   ```bash
   # 创建Cookie文件
   mkdir -p ~/.openclaw/workspace/config/cookies
   vim ~/.openclaw/workspace/config/cookies/xiaohongshu.json
   ```

   ```json
   {
     "cookies": [
       {
         "name": "web_session",
         "value": "粘贴你复制的Cookie值",
         "domain": ".xiaohongshu.com",
         "path": "/",
         "expires": -1,
         "httpOnly": false,
         "secure": true
       }
     ]
   }
   ```

   **注意**：
   - Cookie值是你的账号信息，请妥善保管
   - 不要分享给他人
   - 定期更新Cookie（过期后重新登录导出）

4. **测试Cookie**
   ```bash
   # 使用脚本测试
   python scripts/test-xiaohongshu-cookie.py
   ```

### 其他平台配置

**抖音、B站、微博**：类似流程，参考各平台文档

---

## 3️⃣ 配置OpenClaw环境

### 安装OpenClaw

```bash
# 安装Node.js（如果未安装）
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs

# 安装OpenClaw
npm install -g openclaw

# 初始化
openclaw init
```

### 配置OpenClaw

```bash
# 编辑配置文件
vim ~/.openclaw/openclaw.json
```

```json
{
  "model": "oneapi/AUTO",
  "channel": "infoflow",
  "workspace": "~/.openclaw/workspace"
}
```

### 测试OpenClaw

```bash
# 检查状态
openclaw status

# 测试Skills
openclaw skills list

# 测试Cron
openclaw cron list
```

---

## 4️⃣ 配置图像生成API（可选）

### 即梦API

```bash
# 配置即梦API
JIMENG_API_KEY=xxxxxxxx
JIMENG_API_URL=https://api.jimeng.ai/v1
```

### 其他图像API

**Midjourney**、**DALL-E**：类似配置

---

## 5️⃣ 配置数据库（可选）

### SQLite（推荐）

```bash
# 创建数据库
mkdir -p ~/.openclaw/workspace/data
sqlite3 ~/.openclaw/workspace/data/analytics.db

# 创建表
CREATE TABLE content (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT,
  content TEXT,
  platform TEXT,
  publish_time DATETIME,
  views INTEGER,
  likes INTEGER,
  collects INTEGER,
  shares INTEGER,
  comments INTEGER
);
```

### PostgreSQL（高级）

```bash
# 安装PostgreSQL
sudo apt-get install postgresql

# 创建数据库
sudo -u postgres createdb ai_creator

# 配置连接
vim ~/.openclaw/config/.env
```

```
DATABASE_URL=postgresql://user:password@localhost:5432/ai_creator
```

---

## 📁 目录结构

配置完成后，你的目录应该是：

```
~/.openclaw/
├── openclaw.json              # OpenClaw配置
├── config/
│   ├── .env                   # 环境变量
│   ├── skills/                # Skills配置
│   ├── crons/                 # Cron配置
│   └── rules/                 # Rules配置
│
└── workspace/
    ├── MEMORY.md              # 记忆存储
    ├── USER.md                # 用户信息
    ├── IDENTITY.md            # 身份定位
    └── data/
        ├── analytics.db       # 数据库
        └── reports/           # 报告文件
```

---

## ✅ 验证配置

运行以下命令验证所有配置：

```bash
# 1. 验证LLM API
curl -X POST $ONEAPI_BASE_URL/chat/completions \
  -H "Authorization: Bearer $ONEAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "claude-3-sonnet", "messages": [{"role": "user", "content": "测试"}]}'

# 2. 验证Cookie
python scripts/test-xiaohongshu-cookie.py

# 3. 验证OpenClaw
openclaw status

# 4. 验证数据库
sqlite3 ~/.openclaw/workspace/data/analytics.db "SELECT 1;"
```

---

## 🚨 常见问题

### Q1: API Key无效？

**解决方案**：
1. 检查API Key格式
2. 检查API余额
3. 检查网络连接

### Q2: Cookie过期？

**解决方案**：
1. 重新登录平台
2. 导出新Cookie
3. 更新配置文件

### Q3: OpenClaw安装失败？

**解决方案**：
1. 检查Node.js版本（需要v18+）
2. 使用sudo安装
3. 检查网络连接

---

## 🚀 下一步

环境配置完成！现在：

👉 [学习内容生成](./03-content-generation.md) - 开始生成内容

---

**配置完成时间**：约30分钟
