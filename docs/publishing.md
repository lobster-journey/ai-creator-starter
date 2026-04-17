# 🚀 平台发布实现

> 多平台内容发布系统

---

## 📊 支持平台

| 平台 | 状态 | 发布方式 | 特点 |
|------|------|---------|------|
| 小红书 | ✅ 已实现 | Cookie + 浏览器自动化 | 图文、视频 |
| 抖音 | 🔶 开发中 | Cookie + API | 短视频 |
| B站 | 📋 规划中 | API | 长视频 |
| 微博 | 📋 规划中 | API | 图文 |

---

## 🎯 发布流程

```
内容准备 → 平台适配 → 内容审核 → 定时发布 → 状态追踪
```

---

## 🍎 小红书发布

### 实现原理

**方式一：浏览器自动化**
```
Chrome + Playwright/Rod
↓
模拟用户操作
↓
上传图片/视频
↓
填写内容
↓
点击发布
```

**方式二：API调用**
```
获取平台API
↓
构造请求
↓
调用发布接口
↓
获取发布结果
```

---

### 发布代码示例

```python
# 小红书发布器
class XiaohongshuPublisher:
    def __init__(self, cookie):
        self.cookie = cookie
        self.browser = None

    async def publish(self, title, content, images):
        # 启动浏览器
        self.browser = await launch_browser()

        # 设置Cookie
        await self.browser.set_cookies(self.cookie)

        # 访问发布页面
        await self.browser.goto('https://creator.xiaohongshu.com/publish/publish')

        # 上传图片
        for image in images:
            await self.browser.upload(image)

        # 填写内容
        await self.browser.fill_title(title)
        await self.browser.fill_content(content)

        # 点击发布
        await self.browser.click_publish()

        # 获取结果
        result = await self.browser.get_result()

        return result
```

---

## ⏰ 定时发布

### 发布时间策略

**最佳发布时间**：
- 小红书：10:00, 14:00, 20:00
- 抖音：12:00, 18:00, 21:00
- B站：18:00, 20:00, 22:00

---

### 定时任务配置

```python
# 定时发布配置
PUBLISH_SCHEDULE = {
    'xiaohongshu': {
        'times': ['10:00', '14:00', '20:00'],
        'daily_limit': 3,
        'min_interval': 60  # 分钟
    },
    'douyin': {
        'times': ['12:00', '18:00', '21:00'],
        'daily_limit': 2,
        'min_interval': 120
    }
}
```

---

### 定时任务实现

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

# 添加定时任务
for time in PUBLISH_SCHEDULE['xiaohongshu']['times']:
    hour, minute = map(int, time.split(':'))
    scheduler.add_job(
        publish_to_xiaohongshu,
        'cron',
        hour=hour,
        minute=minute
    )

# 启动调度器
scheduler.start()
```

---

## 🔄 多平台分发

### 分发策略

**方式一：同步发布**
```
一篇内容 → 多个平台同时发布
```

**方式二：差异化发布**
```
一篇内容 → 根据平台特点调整 → 分别发布
```

---

### 平台适配器

```python
class PlatformAdapter:
    @staticmethod
    def adapt(content, platform):
        if platform == 'xiaohongshu':
            return XiaohongshuAdapter().adapt(content)
        elif platform == 'douyin':
            return DouyinAdapter().adapt(content)
        elif platform == 'bilibili':
            return BilibiliAdapter().adapt(content)
```

---

## 📊 发布状态追踪

### 状态类型

- `pending`: 等待发布
- `publishing`: 发布中
- `success`: 发布成功
- `failed`: 发布失败

---

### 状态追踪代码

```python
class PublishTracker:
    def track(self, content_id, platform):
        # 记录发布开始
        self.db.update_status(content_id, 'publishing')

        try:
            # 执行发布
            result = self.publish(content_id, platform)

            # 记录成功
            self.db.update_status(content_id, 'success')
            self.db.save_post_id(content_id, result['post_id'])

        except Exception as e:
            # 记录失败
            self.db.update_status(content_id, 'failed')
            self.db.save_error(content_id, str(e))
```

---

## ⚠️ 发布限制

### 频率限制

| 平台 | 每日上限 | 最小间隔 | 建议频率 |
|------|---------|---------|---------|
| 小红书 | 5篇 | 30分钟 | 2-3篇/天 |
| 抖音 | 3条 | 60分钟 | 1-2条/天 |
| B站 | 2条 | 120分钟 | 1条/天 |

---

### 反爬措施

1. **随机延迟**
   - 每次操作间隔随机时间
   - 模拟真实用户行为

2. **IP轮换**
   - 使用代理池
   - 避免单一IP高频请求

3. **浏览器指纹**
   - 随机User-Agent
   - 随机浏览器特征

---

## 📚 相关文档

- [内容生成](./content-generation.md)
- [自动化运营](./automation.md)
- [数据分析](./analytics.md)

---

**Created by 🦞 Lobster Journey Studio**
