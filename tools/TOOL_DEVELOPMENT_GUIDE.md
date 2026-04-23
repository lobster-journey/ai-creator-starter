# 🛠️ 工具开发规范

## 📋 版本管理

本项目的工具遵循**内部/外部版本分离**原则。

### 版本策略

**内部版本**（Private）
- 位置：lobster-journey-private仓库
- 特点：包含我们的配置，直接可用
- 保护：不提交敏感信息

**外部版本**（Public）
- 位置：本仓库（lobster-journey）
- 特点：需要用户配置自己的信息
- 提供：配置示例和使用说明

---

## 📂 目录结构

```
tools/
├── tool-name/
│   ├── tool.py              # 主程序
│   ├── config.example.json  # 配置示例
│   └── README.md            # 使用说明
```

---

## 🔧 开发流程

### 1. 评估敏感性

开发新工具前，先评估：
- 是否需要账号登录？
- 是否需要API Key？
- 是否包含私密信息？

### 2. 选择策略

**无敏感信息** → 只发布公开版本

**有敏感信息** → 同时维护两个版本：
- 内部版本：直接使用我们的配置
- 外部版本：提供模板，用户自己配置

### 3. 实现分离

**内部版本**（lobster-journey-private）：
```python
# config.json（不提交）
{
  "api_key": "sk-xxxxx",
  "account": "ai-report"
}
```

**外部版本**（lobster-journey）：
```python
# config.example.json（提交）
{
  "api_key": "YOUR_API_KEY",
  "account": "YOUR_ACCOUNT"
}
```

---

## 🔒 安全规则

**绝对禁止提交**：
- ❌ 真实的API Key
- ❌ 真实的密码
- ❌ Cookie文件
- ❌ Token
- ❌ 账号信息

**必须使用.gitignore**：
```gitignore
config.json
*.key
*.token
cookies/
.env
```

---

## 📝 文档要求

每个工具必须包含：
1. **README.md**：使用说明
2. **config.example.json**：配置示例
3. **注释**：代码内详细注释

---

**🦞 龙虾巡游记 | 发现 · 传播 · 陪伴**
