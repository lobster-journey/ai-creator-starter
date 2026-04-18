#!/bin/bash
# 环境初始化脚本

set -e

echo "🚀 开始初始化AI Creator Starter环境..."

# 1. 创建必要的目录
echo "📁 创建目录结构..."
mkdir -p ~/.openclaw/workspace/data
mkdir -p ~/.openclaw/workspace/config/cookies
mkdir -p ~/.openclaw/workspace/config/skills
mkdir -p ~/.openclaw/workspace/config/crons
mkdir -p ~/.openclaw/workspace/logs

# 2. 创建配置文件
echo "⚙️  创建配置文件..."
if [ ! -f ~/.openclaw/workspace/config/.env ]; then
    cat > ~/.openclaw/workspace/config/.env << 'EOF'
# LLM API配置
ONEAPI_API_KEY=your_api_key_here
ONEAPI_BASE_URL=https://api.oneapi.com/v1

# 小红书配置
XIAOHONGSHU_COOKIE=your_cookie_here

# 其他配置
TIMEZONE=Asia/Shanghai
EOF
    echo "✅ 已创建 .env 配置文件模板"
    echo "⚠️  请编辑 ~/.openclaw/workspace/config/.env 填入真实配置"
else
    echo "✅ .env 配置文件已存在"
fi

# 3. 创建记忆文件
echo "📝 创建记忆文件..."
if [ ! -f ~/.openclaw/workspace/MEMORY.md ]; then
    cat > ~/.openclaw/workspace/MEMORY.md << 'EOF'
# 记忆存储

## 用户信息
- 名称：[填写用户信息]
- 偏好：[填写用户偏好]

## 工作习惯
- [填写工作习惯]

## 红线约束
- ❌ 不发布敏感信息
- ❌ 不发布侵权内容
- ✅ 所有内容必须原创
EOF
    echo "✅ 已创建 MEMORY.md 模板"
else
    echo "✅ MEMORY.md 已存在"
fi

# 4. 创建用户文件
echo "👤 创建用户文件..."
if [ ! -f ~/.openclaw/workspace/USER.md ]; then
    cat > ~/.openclaw/workspace/USER.md << 'EOF'
# USER.md - 关于你的主人

- **Name:** [隐私保护]
- **Pronouns:** [填写代词]
- **Timezone:** Asia/Shanghai (GMT+8)
- **Notes:** [填写备注]

## Context

### 关注领域
- [填写关注领域]

### 工作习惯
- [填写工作习惯]

### 红线约束
- ❌ [填写红线约束]
EOF
    echo "✅ 已创建 USER.md 模板"
else
    echo "✅ USER.md 已存在"
fi

# 5. 安装Python依赖（如果有requirements.txt）
if [ -f "requirements.txt" ]; then
    echo "📦 安装Python依赖..."
    pip install -r requirements.txt
fi

# 6. 设置脚本权限
echo "🔐 设置脚本权限..."
chmod +x scripts/*.py 2>/dev/null || true

echo ""
echo "✅ 环境初始化完成！"
echo ""
echo "📋 下一步："
echo "1. 编辑 ~/.openclaw/workspace/config/.env 填入API密钥"
echo "2. 运行 scripts/collect-hotspots.py 测试热点采集"
echo "3. 运行 scripts/generate-content.py 测试内容生成"
echo "4. 配置定时任务，实现自动化运营"
echo ""
echo "🦞 祝你运营成功！"
