---
name: jimeng-api-scheduler
description: 即梦API图像生成服务。支持文生图、图生图，2K/4K分辨率，多种比例。当用户要求"用即梦生成图片"、"AI画图"、"文生图"时使用此skill。API服务端口5100，已配置Session ID认证。
---

# 即梦API图像生成服务

通过即梦AI API生成高质量图片，支持多种分辨率和比例。

## ✅ 服务状态

- **API地址**：http://localhost:5100
- **服务状态**：运行中 ✅
- **Session ID**：已配置（有效期至登录失效）
- **默认模型**：jimeng-4.5
- **默认分辨率**：2k
- **默认比例**：16:9

## 🎯 核心功能

### 1. 文生图（Text-to-Image）

根据文字描述生成图片。

**API调用示例**：
```bash
curl -X POST http://localhost:5100/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_SESSION_ID" \
  -d '{
    "model": "jimeng-4.5",
    "prompt": "一只可爱的小龙虾在海底探索，卡通风格",
    "ratio": "16:9",
    "resolution": "2k"
  }'
```

**参数说明**：
- `model`：模型名称（jimeng-4.5、jimeng-image-4.5）
- `prompt`：图片描述（中文支持）
- `ratio`：图片比例
- `resolution`：分辨率（1k、2k、4k）

### 2. 图生图（Image-to-Image）

根据参考图生成新图片。

**API调用示例**：
```bash
curl -X POST http://localhost:5100/v1/images/compositions \
  -H "Authorization: Bearer YOUR_SESSION_ID" \
  -F "prompt=根据参考图生成新的图片" \
  -F "model=jimeng-4.5" \
  -F "ratio=16:9" \
  -F "resolution=2k" \
  -F "images=@/path/to/reference.png"
```

## 📐 支持的参数

### 分辨率 (resolution)

| 值 | 尺寸 | 说明 |
|----|------|------|
| `1k` | 1024x1024 | 默认，速度快 |
| `2k` | 2048x2048 | 推荐，质量好 |
| `4k` | 4096x4096 | 高清，耗时长 |

### 比例 (ratio)

| 值 | 适用场景 |
|----|---------|
| `1:1` | 正方形，头像、图标 |
| `16:9` | 宽屏，横版封面、视频封面 |
| `9:16` | 竖屏，手机壁纸、小红书笔记 |
| `4:3` | 横向，演示文稿 |
| `3:4` | 纵向，海报、宣传图 |
| `3:2` | 经典横向，摄影 |
| `2:3` | 经典纵向，杂志 |
| `21:9` | 超宽屏，电影感 |

### 模型 (model)

- `jimeng-4.5`：最新旗舰模型（推荐）
- `jimeng-image-4.5`：图像生成专用模型

## 🚀 快速使用

### Python脚本方式

创建简单的调用脚本：

```python
import requests
import os
from dotenv import load_dotenv

# 加载配置
load_dotenv('~/.openclaw/workspace/config/jimeng/config.env')

# API配置
API_URL = os.getenv('JIMENG_API_URL', 'http://localhost:5100')
SESSION_ID = os.getenv('JIMENG_SESSION_ID')

# 生成图片
def generate_image(prompt, ratio='16:9', resolution='2k', model='jimeng-4.5'):
    """生成图片"""
    response = requests.post(
        f'{API_URL}/v1/images/generations',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {SESSION_ID}'
        },
        json={
            'model': model,
            'prompt': prompt,
            'ratio': ratio,
            'resolution': resolution
        },
        timeout=60
    )
    
    result = response.json()
    
    if 'data' in result:
        return [img['url'] for img in result['data']]
    else:
        raise Exception(f"生成失败: {result}")
    
# 使用示例
if __name__ == '__main__':
    urls = generate_image('一只可爱的小龙虾在海底探索')
    for i, url in enumerate(urls, 1):
        print(f'图片{i}: {url}')
```

### cURL命令方式

```bash
# 快速生成（使用配置文件中的Session ID）
SESSION_ID=$(grep JIMENG_SESSION_ID ~/.openclaw/workspace/config/jimeng/config.env | cut -d'=' -f2)

curl -X POST http://localhost:5100/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $SESSION_ID" \
  -d '{"model":"jimeng-4.5","prompt":"你的描述","ratio":"16:9","resolution":"2k"}'
```

## ⚙️ 配置管理

### 配置文件位置

`~/.openclaw/workspace/config/jimeng/config.env`

### 配置内容

```bash
# 即梦API配置
JIMENG_SESSION_ID=your_session_id_here
JIMENG_API_URL=http://localhost:5100
JIMENG_DEFAULT_MODEL=jimeng-4.5
JIMENG_DEFAULT_RESOLUTION=2k
JIMENG_DEFAULT_RATIO=16:9
```

### 获取Session ID

1. 访问即梦官网：https://jimeng.jianying.com/
2. 登录账号
3. 打开浏览器开发者工具（F12）
4. Application → Storage → Cookies → `sessionid`
5. 复制值并更新配置文件

## 🔧 服务管理

### 检查服务状态

```bash
curl http://localhost:5100/ping
```

预期返回：`pong`

### 启动服务

如果服务未运行：

```bash
cd ~/workspace/jimeng-api
npm run dev > /tmp/jimeng.log 2>&1 &
```

### 停止服务

```bash
ps aux | grep 'node.*jimeng' | grep -v grep | awk '{print $2}' | xargs kill -9
```

### 查看日志

```bash
tail -f /tmp/jimeng.log
```

## 📊 成本说明

- **积分消耗**：3积分/张（文生图）
- **视频生成**：210积分/次
- **每日赠送**：66积分（登录奖励）
- **会员权益**：标准会员额外积分

## 🎨 最佳实践

### 小红书笔记配图

推荐参数：
- `ratio`: `9:16` 或 `3:4`（竖屏）
- `resolution`: `2k`（质量与速度平衡）
- 提示词：详细描述主体、风格、氛围

### 视频封面

推荐参数：
- `ratio`: `16:9`（横版宽屏）
- `resolution`: `2k` 或 `4k`
- 提示词：突出主体，电影感

### PPT配图

推荐参数：
- `ratio`: `16:9` 或 `4:3`
- `resolution`: `2k`
- 提示词：专业、简洁、商务风格

## ⚠️ 注意事项

1. **Session ID有效期**：登录失效后需重新获取
2. **积分不足**：检查积分余额，每日登录可获取积分
3. **网络问题**：确保能访问即梦服务器
4. **生成时间**：1k约20-30秒，2k约30-40秒，4k约60-90秒
5. **图片链接有效期**：生成后尽快下载，链接有时效限制

## 📚 参考资料

详细的安装配置和高级用法，请查看：
- **即梦API配置指南**: references/jimeng-api-setup.md

## 🔄 更新日志

- **2026-04-21**: 整理目录结构，补充实际使用方法，测试验证成功
- **初始版本**: 定时管理器功能
