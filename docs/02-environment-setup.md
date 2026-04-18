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

### 方式一：使用OneAPI（推荐）

**优点**：
- 统一接口
- 多模型切换
- 成本可控

**步骤**：
1. 注册OneAPI账号
2. 获取API Key
3. 配置到环境变量

```bash
# 编辑配置文件
vim ~/.openclaw/config/.env

# 添加以下内容
ONEAPI_API_KEY=sk-xxxxxxxx
ONEAPI_BASE_URL=https://api.oneapi.com/v1
```

### 方式二：直接使用LLM API

**Claude API**：
```bash
ANTHROPIC_API_KEY=sk-ant-xxxxxxxx
```

**GPT API**：
```bash
OPENAI_API_KEY=sk-xxxxxxxx
OPENAI_BASE_URL=https://api.openai.com/v1
```

**GLM API**：
```bash
GLM_API_KEY=xxxxxxxx
GLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4
```

### 测试API

```bash
# 测试OneAPI
curl -X POST https://api.oneapi.com/v1/chat/completions \
  -H "Authorization: Bearer $ONEAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-3-sonnet",
    "messages": [{"role": "user", "content": "测试"}]
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
   - 切换到Network标签
   - 刷新页面
   - 找到任意请求
   - 复制Cookie值

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
         "value": "你的Cookie值",
         "domain": ".xiaohongshu.com",
         "path": "/",
         "expires": -1,
         "httpOnly": false,
         "secure": true
       }
     ]
   }
   ```

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
