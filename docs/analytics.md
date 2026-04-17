# 📊 数据分析

> 数据驱动的增长体系

---

## 📈 数据采集

### 采集维度

1. **内容数据**
   - 阅读量
   - 点赞数
   - 收藏数
   - 评论数
   - 分享数

2. **用户数据**
   - 粉丝增长
   - 用户画像
   - 活跃时间

3. **平台数据**
   - 推荐量
   - 曝光量
   - 点击率

---

### 采集方式

**方式一：API采集**
```python
# 小红书数据采集
def fetch_stats(post_id):
    url = f"https://creator.xiaohongshu.com/api/post/{post_id}/stats"
    response = requests.get(url, cookies=cookies)
    return response.json()
```

**方式二：浏览器自动化**
```python
# 模拟登录后采集
async def fetch_stats(post_id):
    await browser.goto(f"https://www.xiaohongshu.com/post/{post_id}")
    stats = await browser.get_stats()
    return stats
```

---

## 💾 数据存储

### 数据库设计

**统计表**：
```sql
CREATE TABLE stats (
    id INTEGER PRIMARY KEY,
    content_id INTEGER,
    platform TEXT,
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    collected INTEGER DEFAULT 0,
    stat_time DATETIME,
    created_at DATETIME
);
```

**粉丝表**：
```sql
CREATE TABLE followers (
    id INTEGER PRIMARY KEY,
    platform TEXT,
    count INTEGER,
    date DATE,
    created_at DATETIME
);
```

---

## 📊 数据分析

### 关键指标

**内容指标**：
- **互动率** = (点赞+收藏+评论+分享) / 阅读量
- **收藏率** = 收藏数 / 阅读量
- **分享率** = 分享数 / 阅读量

**增长指标**：
- **粉丝增长率** = (今日粉丝 - 昨日粉丝) / 昨日粉丝
- **内容增长率** = 本周内容数 / 上周内容数

---

### 分析维度

1. **时间维度**
   - 小时分布
   - 日期趋势
   - 周期性分析

2. **内容维度**
   - 主题对比
   - 形式对比
   - 长度对比

3. **平台维度**
   - 平台对比
   - 跨平台分析

---

### 分析代码

```python
import pandas as pd
import matplotlib.pyplot as plt

# 数据分析
def analyze_stats(stats_df):
    # 计算互动率
    stats_df['engagement_rate'] = (
        stats_df['likes'] + stats_df['comments'] + stats_df['shares']
    ) / stats_df['views']

    # 按主题分组
    topic_stats = stats_df.groupby('topic').agg({
        'views': 'mean',
        'engagement_rate': 'mean'
    }).sort_values('views', ascending=False)

    return topic_stats

# 可视化
def visualize_stats(stats_df):
    plt.figure(figsize=(12, 6))
    plt.plot(stats_df['date'], stats_df['views'])
    plt.title('阅读量趋势')
    plt.xlabel('日期')
    plt.ylabel('阅读量')
    plt.show()
```

---

## 📋 数据报告

### 日报模板

```markdown
# 数据日报 - {date}

## 昨日数据
- 发布内容：{count}篇
- 总阅读：{views}
- 总互动：{engagement}
- 粉丝增长：{followers}

## 热门内容
1. {title} - {views}阅读
2. {title} - {views}阅读
3. {title} - {views}阅读

## 分析与建议
{analysis}
```

---

### 周报模板

```markdown
# 数据周报 - Week {week}

## 本周数据
- 发布内容：{count}篇
- 总阅读：{views}
- 总互动：{engagement}
- 粉丝增长：{followers}

## 内容效果分析
{content_analysis}

## 热门内容TOP5
{top_contents}

## 用户画像分析
{user_analysis}

## 优化建议
{suggestions}

## 下周计划
{next_week_plan}
```

---

## 🎯 数据驱动优化

### 优化方向

1. **内容优化**
   - 分析热门内容特征
   - 调整内容方向
   - 优化标题和配图

2. **发布优化**
   - 分析最佳发布时间
   - 调整发布频率
   - 优化发布策略

3. **用户优化**
   - 分析用户画像
   - 调整内容定位
   - 增加用户互动

---

### 优化流程

```
数据采集 → 数据分析 → 发现问题 → 制定策略 → 执行优化 → 效果验证
```

---

## 📚 相关文档

- [内容生成](./content-generation.md)
- [平台发布](./publishing.md)
- [自动化运营](./automation.md)

---

**Created by 🦞 Lobster Journey Studio**
