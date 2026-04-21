# 即梦API配置指南

本文档提供即梦API服务的详细配置和使用说明。

## 即梦API简介

即梦API是基于字节跳动即梦AI的逆向工程实现，提供与OpenAI API兼容的接口格式，支持：
- AI图像生成（文生图、图生图）
- AI视频生成
- 多模型支持（jimeng-4.5等）
- 2K/4K分辨率

## 环境要求

- Node.js 18+
- npm 或 yarn
- Git

## 安装步骤

### 1. 克隆仓库

```bash
cd /home/gem/workspace
git clone https://github.com/iptag/jimeng-api.git
cd jimeng-api
```

### 2. 安装依赖

```bash
npm install
```

### 3. 构建项目

```bash
npm run build
```

### 4. 启动服务

```bash
# 开发模式（带热重载）
npm run dev

# 生产模式
npm start
```

服务默认运行在 `http://localhost:5100`

### 5. 验证服务

```bash
curl http://localhost:5100/ping
```

预期返回：`pong`

## 获取Session ID

### 方法1：浏览器开发者工具

1. 访问即梦官网：https://jimeng.jianying.com/
2. 登录账号
3. 打开浏览器开发者工具（F12）
4. 切换到 Application 标签
5. 在左侧找到 Storage → Cookies
6. 找到 `sessionid` 字段，复制其值

### 方法2：网络请求拦截

1. 打开浏览器开发者工具（F12）
2. 切换到 Network 标签
3. 在即梦网站执行一次图片生成操作
4. 在网络请求中找到API请求
5. 查看请求头中的 `Authorization` 字段
6. 提取 `Bearer` 后面的值（即sessionid）

## API使用示例

### 文生图

```bash
curl -X POST http://localhost:5100/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_SESSION_ID" \
  -d '{
    "model": "jimeng-4.5",
    "prompt": "一个美丽的女孩，电影感",
    "ratio": "16:9",
    "resolution": "2k"
  }'
```

### 图生图

```bash
curl -X POST http://localhost:5100/v1/images/compositions \
  -H "Authorization: Bearer YOUR_SESSION_ID" \
  -F "prompt=根据参考图生成新的图片" \
  -F "model=jimeng-4.5" \
  -F "ratio=16:9" \
  -F "resolution=2k" \
  -F "images=@/path/to/reference.png"
```

## 支持的参数

### 分辨率 (resolution)

- `1k`: 1024x1024 (默认)
- `2k`: 2048x2048
- `4k`: 4096x4096

### 比例 (ratio)

- `1:1`: 正方形
- `4:3`: 横向
- `3:4`: 纵向
- `16:9`: 宽屏
- `9:16`: 竖屏
- `3:2`: 经典横向
- `2:3`: 经典纵向
- `21:9`: 超宽屏

### 模型 (model)

- `jimeng-4.5`: 最新旗舰模型（推荐）
- `jimeng-image-4.5`: 图像生成专用模型

## 常见问题

### 服务启动失败

检查端口是否被占用：
```bash
lsof -i :5100
```

### Session ID无效

- 确认Session ID是否正确复制
- Session ID可能过期，需要重新获取
- 检查即梦账号是否正常登录

### 图片生成失败

- 检查积分是否充足（即梦每日赠送66积分）
- 检查网络连接
- 查看服务日志：`tail -f /tmp/jimeng.log`

## 服务管理

### 启动服务

```bash
cd /home/gem/workspace/jimeng-api
npm run dev > /tmp/jimeng.log 2>&1 &
```

### 停止服务

```bash
# 查找进程
ps aux | grep 'node.*jimeng' | grep -v grep

# 终止进程
ps aux | grep 'node.*jimeng' | grep -v grep | awk '{print $2}' | xargs kill -9
```

### 查看日志

```bash
tail -f /tmp/jimeng.log
```

## 定时任务配置

通过定时任务自动管理服务的启动和停止，详见主SKILL.md中的步骤4。