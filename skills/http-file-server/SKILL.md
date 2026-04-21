# 沙箱文件分享 Skill

## 📝 功能描述

让人类能够访问龙虾沙箱环境中的所有文件，通过HTTP服务器提供文件下载链接。

**核心能力**：
- 🌐 HTTP文件服务器（端口8194）
- 📦 支持所有文件类型访问
- 🔤 UTF-8强制编码（解决中文乱码）
- 📂 支持多层子目录访问
- 🔄 长期后台运行

---

## 🎯 使用场景

### 何时使用此Skill

**❌ 图片文件**：不使用此Skill
- 直接通过 `infoflow_send` 发送到聊天窗口
- 参数：`imageUrl="本地文件绝对路径"`

**✅ 其他类型文件**：使用此Skill
- 文档文件（.md, .txt, .pdf, .doc）
- 代码文件（.py, .js, .java, .go）
- 数据文件（.csv, .json, .xml, .yaml）
- 配置文件（.env, .conf, .ini）
- 压缩文件（.zip, .tar, .gz）

---

## 🚀 快速开始

### 1. 启动服务器

```bash
bash ~/.openclaw/skills/sandbox-file-sharing/scripts/start_server.sh
```

### 2. 生成文件访问链接

**格式**：
```
https://${PORT}-${SANDBOX_ID}.agent-sandbox.${ENTERPRISE_DOMAIN}/文件相对路径
```

**配置文件**：`config/server.conf`
- 包含敏感信息（企业域名、沙箱ID）
- 请勿将配置文件提交到外部仓库

**示例**：
```
📄 MEMORY.md
https://${PORT}-${SANDBOX_ID}.agent-sandbox.${ENTERPRISE_DOMAIN}/MEMORY.md

💻 scripts/jimeng_generate.py
https://${PORT}-${SANDBOX_ID}.agent-sandbox.${ENTERPRISE_DOMAIN}/scripts/jimeng_generate.py

📊 data/report.csv
https://${PORT}-${SANDBOX_ID}.agent-sandbox.${ENTERPRISE_DOMAIN}/data/report.csv
```

### 3. 发送给用户

```
📄 文件已准备好，下载地址：
https://${PORT}-${SANDBOX_ID}.agent-sandbox.${ENTERPRISE_DOMAIN}/文件路径
```

**注意**：实际使用时需从 `config/server.conf` 读取配置替换占位符

---

## 📂 文件访问规则

### 服务目录

**根目录**：`~/.openclaw/workspace/`

**访问映射**：
- 本地路径：`~/.openclaw/workspace/MEMORY.md`
- 访问地址：`https://${PORT}-${SANDBOX_ID}.agent-sandbox.${ENTERPRISE_DOMAIN}/MEMORY.md`

- 本地路径：`~/.openclaw/workspace/scripts/file.py`
- 访问地址：`https://${PORT}-${SANDBOX_ID}.agent-sandbox.${ENTERPRISE_DOMAIN}/scripts/file.py`

### 支持的文件类型

**文本文件**（UTF-8编码）：
- .md, .txt, .html, .css, .js, .json, .xml, .yaml, .yml
- .py, .java, .go, .c, .cpp, .h, .sh, .bat
- .csv, .tsv, .sql, .conf, .ini, .env

**二进制文件**：
- .pdf, .doc, .docx, .xls, .xlsx, .ppt, .pptx
- .zip, .tar, .gz, .rar, .7z
- .jpg, .png, .gif, .svg（但图片建议直接发送）

---

## 🛠️ 服务器管理

### 启动服务器

```bash
bash ~/.openclaw/skills/sandbox-file-sharing/scripts/start_server.sh
```

### 停止服务器

```bash
kill $(cat /tmp/file_server.pid)
```

### 重启服务器

```bash
bash ~/.openclaw/skills/sandbox-file-sharing/scripts/start_server.sh
```

### 检查状态

```bash
ps aux | grep "utf8_file_server"
netstat -tlnp | grep 8194
```

---

## ⚙️ 技术实现

### 服务器架构

**核心脚本**：
- `scripts/start_server.sh` - 启动脚本
- `scripts/utf8_file_server.py` - UTF-8强制编码HTTP服务器

**配置参数**：
- 端口：8194
- 服务目录：`~/.openclaw/workspace/`
- PID文件：`/tmp/file_server.pid`
- 日志文件：`/tmp/file_server.log`

### UTF-8编码实现

**问题**：浏览器访问文本文件时可能显示乱码

**解决方案**：
- HTTP响应头强制包含 `charset=utf-8`
- 示例：`Content-Type: text/markdown; charset=utf-8`

**支持编码类型**：
```python
mimetypes.add_type('text/markdown; charset=utf-8', '.md')
mimetypes.add_type('text/plain; charset=utf-8', '.txt')
mimetypes.add_type('text/html; charset=utf-8', '.html')
# ... 更多类型
```

---

## 🔧 常见问题

### 问题1：502 Bad Gateway

**原因**：服务器状态异常或未运行

**解决**：
```bash
bash ~/.openclaw/skills/sandbox-file-sharing/scripts/start_server.sh
```

### 问题2：Empty reply from server

**原因**：端口被占用

**解决**：
```bash
lsof -ti:8194 | xargs kill -9
bash ~/.openclaw/skills/sandbox-file-sharing/scripts/start_server.sh
```

### 问题3：文件访问404

**原因**：文件不在workspace目录下

**解决**：将文件复制到 `~/.openclaw/workspace/` 目录

### 问题4：中文乱码

**原因**：浏览器未自动识别编码

**解决**：
1. 浏览器右键 → 编码 → UTF-8
2. 或下载后用本地编辑器打开

---

## 📝 使用示例

### 示例1：发送Markdown文档

```
📄 MEMORY.md 已更新

下载地址：https://${PORT}-${SANDBOX_ID}.agent-sandbox.${ENTERPRISE_DOMAIN}/MEMORY.md
```

### 示例2：发送代码文件

```
💻 即梦图像生成脚本已优化

文件：jimeng_generate.py
下载地址：https://${PORT}-${SANDBOX_ID}.agent-sandbox.${ENTERPRISE_DOMAIN}/scripts/jimeng_generate.py
```

### 示例3：发送配置文件

```
⚙️ 配置文件已更新

文件：config/jimeng/config.env
下载地址：https://${PORT}-${SANDBOX_ID}.agent-sandbox.${ENTERPRISE_DOMAIN}/config/jimeng/config.env
```

---

## ⚠️ 注意事项

1. **文件位置**：文件必须在 `~/.openclaw/workspace/` 目录下
2. **安全限制**：不要分享敏感配置文件（API Key、密码等）
3. **图片文件**：建议直接发送，不走HTTP服务
4. **服务持久化**：服务器使用 `nohup` 启动，会话结束后继续运行
5. **编码问题**：已强制UTF-8，如仍有乱码请下载后本地查看

---

## 📅 更新日志

- **2026-04-21 16:50**：创建sandbox-file-sharing Skill，整合HTTP文件分享功能
- **2026-04-21 16:28**：完善UTF-8编码解决方案
- **2026-04-21 16:10**：建立HTTP文件服务器

---

## 🔗 相关文档

- `docs/TROUBLESHOOTING.md` - 详细问题排查
- `docs/FILE_TYPES.md` - 支持的文件类型列表
