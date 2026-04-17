# 实施步骤详解

本文档详细说明从0到1搭建AI内容创作系统的每一步。

---

## 总览

```
Step 1: 账号准备 → Step 2: 内容生成 → Step 3: 平台发布 → Step 4: 数据分析 → Step 5: 自动化运营
```

---

## Step 1: 账号准备

### 1.1 平台账号注册

**目标平台**：
- 小红书（主要）
- 抖音（次要）
- B站（次要）
- 微博（辅助）

**注册注意事项**：
- ✅ 使用常用手机号
- ✅ 完善个人资料
- ✅ 明确账号定位
- ❌ 避免违规历史

---

### 1.2 Cookie导出

**为什么需要Cookie？**
- AI智能体无GUI界面
- 无法扫码登录
- Cookie是最简单的认证方式

**导出步骤**（以Chrome为例）：

#### 方法1：开发者工具导出

```
1. 打开小红书网站并登录
2. 按F12打开开发者工具
3. 切换到"Application"标签
4. 左侧选择"Cookies" → "https://www.xiaohongshu.com"
5. 复制所有Cookie
```

#### 方法2：使用插件导出

推荐插件：
- **Cookie Editor**（Chrome/Firefox）
- **EditThisCookie**（Chrome）

导出格式：
```json
[
  {
    "name": "a1",
    "value": "19d9a3d2020wk7yp574islowa4treq1zkmc3y2d2j30000436516",
    "domain": ".xiaohongshu.com",
    "path": "/",
    "expires": 1807945190,
    "httpOnly": false,
    "secure": false
  },
  {
    "name": "web_session",
    "value": "040069b8958cb980a8da2a93d43b4b7b40db43",
    "domain": ".xiaohongshu.com",
    "path": "/",
    "expires": 1807945411,
    "httpOnly": true,
    "secure": true
  }
  // ... 其他Cookie
]
```

**关键Cookie字段**：
- `a1` - 身份标识
- `web_session` - 会话令牌
- `websectiga` - 安全令牌
- `id_token` - ID令牌

---

### 1.3 Cookie存储

**安全存储方案**：

```python
from cryptography.fernet import Fernet
import json

# 生成加密密钥（仅需一次）
key = Fernet.generate_key()
# 保存密钥到安全位置

# 加密Cookie
def encrypt_cookies(cookies, key):
    f = Fernet(key)
    encrypted = f.encrypt(json.dumps(cookies).encode())
    with open('config/cookies/xiaohongshu.enc', 'wb') as file:
        file.write(encrypted)

# 解密Cookie
def decrypt_cookies(key):
    f = Fernet(key)
    with open('config/cookies/xiaohongshu.enc', 'rb') as file:
        encrypted = file.read()
    return json.loads(f.decrypt(encrypted).decode())
```

**存储位置**：
```
config/
├── cookies/
│   ├── xiaohongshu.enc  # 加密的小红书Cookie
│   ├── douyin.enc        # 加密的抖音Cookie
│   └── bilibili.enc      # 加密的B站Cookie
└── .env                  # 环境变量（包含密钥）
```

---

### 1.4 API密钥配置

**需要的API密钥**：

1. **LLM API密钥**
   - OneAPI令牌（推荐）
   - 或直接使用Claude/GPT API密钥

```bash
# .env 文件
LLM_PROVIDER=oneapi
LLM_API_KEY=sk-xxxx
LLM_API_BASE=https://api.oneapi.com/v1
LLM_MODEL=claude-3-5-sonnet-20241022
```

2. **图像生成API密钥**（可选）
   - 即梦（Dreamina）
   - Midjourney
   - DALL-E

```bash
IMAGE_PROVIDER=dreamina
DREAMINA_API_KEY=xxxx
```

---

### 1.5 Cookie有效性验证

**验证脚本**：

```python
import requests

def validate_xiaohongshu_cookie(cookies):
    """
    验证小红书Cookie是否有效
    """
    session = requests.Session()
    
    # 添加Cookie
    for cookie in cookies:
        session.cookies.set(
            cookie['name'],
            cookie['value'],
            domain=cookie.get('domain', '.xiaohongshu.com'),
            path=cookie.get('path', '/')
        )
    
    try:
        # 访问需要登录的页面
        response = session.get(
            'https://creator.xiaohongshu.com/',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        
        # 检查是否跳转到登录页
        if 'login' in response.url:
            return {
                'valid': False,
                'message': 'Cookie已过期，请重新导出'
            }
        
        # 检查是否能访问创作者中心
        if response.status_code == 200:
            return {
                'valid': True,
                'message': 'Cookie有效'
            }
        else:
            return {
                'valid': False,
                'message': f'访问失败: HTTP {response.status_code}'
            }
    
    except Exception as e:
        return {
            'valid': False,
            'message': f'验证异常: {str(e)}'
        }

# 使用示例
cookies = json.load(open('config/cookies/xiaohongshu.json'))
result = validate_xiaohongshu_cookie(cookies)
print(result)
```

---

## Step 2: 内容生成

### 2.1 选题生成

**选题来源**：
1. 热点追踪（微博热搜、知乎热榜等）
2. 用户兴趣（AI、科技、大模型等）
3. 数据分析（爆款内容分析）
4. 竞品分析（同类账号内容）

**实现代码**：

```python
def generate_topics(interests, hot_topics):
    """
    生成选题
    
    Args:
        interests: 用户兴趣列表
        hot_topics: 当前热点列表
    
    Returns:
        选题列表
    """
    prompt = f"""
你是一个专业的科技博主选题助手。

用户兴趣：{', '.join(interests)}
当前热点：{', '.join(hot_topics)}

请生成5个小红书选题，要求：
1. 结合用户兴趣和当前热点
2. 有话题性和传播性
3. 原创不抄袭
4. 符合AI科技博主定位

格式：
1. 【标题】选题标题
   - 关键词：xxx
   - 推荐理由：xxx
"""
    
    response = llm_api.generate(prompt)
    return parse_topics(response)
```

---

### 2.2 文案生成

**小红书文案特点**：
- 标题：吸引眼球，带emoji
- 正文：300-500字，分段清晰
- 标签：3-5个相关标签
- 表情：适当使用emoji

**实现代码**：

```python
def generate_xiaohongshu_note(topic, style="professional_casual"):
    """
    生成小红书笔记
    
    Args:
        topic: 选题
        style: 风格（professional_casual/fun_energetic/serious_educational）
    
    Returns:
        笔记内容
    """
    style_prompts = {
        "professional_casual": "专业但亲切，有深度但不晦涩",
        "fun_energetic": "活泼有趣，轻松愉快",
        "serious_educational": "严肃教育，深度分析"
    }
    
    prompt = f"""
你是一个专业的AI科技博主，正在为小红书创作内容。

选题：{topic}
风格：{style_prompts[style]}

请创作一篇小红书笔记，要求：

【标题】
- 吸引眼球，20字以内
- 包含关键词
- 适当使用emoji

【正文】
- 300-500字
- 分3-5段
- 每段1-2个重点
- 适当使用emoji
- 可以使用列表、引用等格式

【标签】
- 3-5个相关标签
- 包含热门标签和垂直标签

现在开始创作：
"""
    
    response = llm_api.generate(prompt)
    
    # 解析返回内容
    note = {
        'title': extract_title(response),
        'content': extract_content(response),
        'tags': extract_tags(response)
    }
    
    return note
```

---

### 2.3 内容审核

**审核维度**：
1. 敏感词检测
2. 原创性检查
3. 合规性验证

**实现代码**：

```python
# 敏感词库
SENSITIVE_WORDS = [
    # 政治
    "xxx", "yyy",
    # 违法
    "zzz", "aaa",
    # 低俗
    "bbb", "ccc"
]

def check_sensitive_words(text):
    """
    敏感词检测
    """
    found_words = []
    for word in SENSITIVE_WORDS:
        if word in text:
            found_words.append(word)
    
    if found_words:
        return {
            'pass': False,
            'reason': f'包含敏感词: {", ".join(found_words)}'
        }
    
    return {
        'pass': True,
        'reason': '无敏感词'
    }

def check_originality(text):
    """
    原创性检查
    """
    # 可以使用查重API
    # 或使用LLM进行判断
    
    prompt = f"""
请判断以下内容是否为原创：

{text}

要求：
1. 如果是明显的抄袭或翻译，返回 "非原创"
2. 如果是原创或有深度改写，返回 "原创"
3. 给出简短理由

格式：
判断：原创/非原创
理由：xxx
"""
    
    response = llm_api.generate(prompt)
    
    if '非原创' in response:
        return {
            'pass': False,
            'reason': '内容疑似非原创'
        }
    
    return {
        'pass': True,
        'reason': '内容原创'
    }

def review_content(note):
    """
    内容审核
    """
    # 1. 敏感词检测
    result = check_sensitive_words(note['title'] + note['content'])
    if not result['pass']:
        return result
    
    # 2. 原创性检查
    result = check_originality(note['content'])
    if not result['pass']:
        return result
    
    # 3. 其他检查...
    
    return {
        'pass': True,
        'reason': '内容审核通过'
    }
```

---

### 2.4 图像生成

**推荐工具**：
- 即梦（Dreamina）- 国内访问友好
- Midjourney - 质量高
- DALL-E 3 - 文字理解好

**实现代码**：

```python
def generate_image_for_note(note):
    """
    为笔记生成配图
    
    Args:
        note: 笔记内容
    
    Returns:
        图片URL列表
    """
    # 提取关键词
    keywords = extract_keywords(note['title'] + ' ' + note['content'])
    
    # 生成提示词
    prompt = f"""
AI科技风格插图，
关键词：{', '.join(keywords)}，
风格：现代、科技、简约，
颜色：蓝色、紫色、白色，
分辨率：1080x1440
"""
    
    # 调用图像生成API
    image_url = dreamina_api.generate(prompt)
    
    return [image_url]
```

---

## Step 3: 平台发布

### 3.1 发布方案选择

#### 方案A：纯API发布（推荐）

**优点**：
- 无需浏览器
- 速度快
- 资源占用少

**缺点**：
- 需要逆向工程API
- 可能被平台更新影响

**实现**：

```python
import requests
import json
import time

class XiaohongshuAPIPublisher:
    def __init__(self, cookies):
        self.session = requests.Session()
        self.base_url = "https://edith.xiaohongshu.com"
        
        # 添加Cookie
        for cookie in cookies:
            self.session.cookies.set(
                cookie['name'],
                cookie['value'],
                domain=cookie.get('domain', '.xiaohongshu.com')
            )
        
        # 设置请求头
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://creator.xiaohongshu.com/',
            'Origin': 'https://creator.xiaohongshu.com'
        })
    
    def upload_image(self, image_path):
        """
        上传图片
        """
        url = f"{self.base_url}/api/sns/web/v1/upload/image"
        
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = self.session.post(url, files=files)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('data', {}).get('url')
        else:
            raise Exception(f"上传失败: {response.text}")
    
    def publish_note(self, title, content, images, tags):
        """
        发布笔记
        
        Args:
            title: 标题
            content: 正文
            images: 图片URL列表
            tags: 标签列表
        
        Returns:
            发布结果
        """
        url = f"{self.base_url}/api/sns/web/v1/note/post"
        
        data = {
            "title": title,
            "desc": content,
            "type": "normal",
            "video": None,
            "images": images,
            "topics": tags,
            "ats": [],
            "is_post": True
        }
        
        response = self.session.post(
            url,
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                return {
                    'success': True,
                    'note_id': result.get('data', {}).get('note_id'),
                    'message': '发布成功'
                }
            else:
                return {
                    'success': False,
                    'message': result.get('msg', '发布失败')
                }
        else:
            raise Exception(f"请求失败: {response.text}")
```

#### 方案B：Headless浏览器发布

**优点**：
- 模拟真人操作
- 不易被检测
- 兼容性好

**缺点**：
- 需要安装浏览器
- 资源占用较大
- 速度较慢

**实现**：

```python
from playwright.sync_api import sync_playwright
import time

class XiaohongshuBrowserPublisher:
    def __init__(self, cookies, headless=True):
        self.cookies = cookies
        self.headless = headless
    
    def publish_note(self, title, content, images, tags):
        """
        使用浏览器发布笔记
        """
        with sync_playwright() as p:
            # 启动浏览器
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context()
            
            # 注入Cookie
            context.add_cookies(self.cookies)
            
            page = context.new_page()
            
            try:
                # 访问发布页面
                page.goto('https://creator.xiaohongshu.com/publish/publish')
                page.wait_for_load_state('networkidle')
                
                # 上传图片
                for i, image_path in enumerate(images):
                    if i == 0:
                        # 第一张图片
                        page.locator('input[type="file"]').first.set_input_files(image_path)
                    else:
                        # 后续图片
                        page.locator('button:has-text("继续上传")').click()
                        page.locator('input[type="file"]').last.set_input_files(image_path)
                    
                    # 等待上传完成
                    time.sleep(2)
                
                # 填写标题
                page.fill('[placeholder="填写标题"]', title)
                
                # 填写正文
                page.fill('[placeholder="填写正文"]', content)
                
                # 添加标签
                for tag in tags:
                    page.click('button:has-text("添加标签")')
                    page.fill('input[placeholder="搜索标签"]', tag)
                    time.sleep(1)
                    page.click(f'text={tag}')
                
                # 发布
                page.click('button:has-text("发布")')
                
                # 等待发布完成
                page.wait_for_selector('text=发布成功', timeout=30000)
                
                return {
                    'success': True,
                    'message': '发布成功'
                }
            
            except Exception as e:
                return {
                    'success': False,
                    'message': str(e)
                }
            
            finally:
                browser.close()
```

---

### 3.2 发布流程

```python
def publish_workflow(note, images, publisher):
    """
    完整发布流程
    """
    # 1. 内容审核
    review_result = review_content(note)
    if not review_result['pass']:
        return {
            'success': False,
            'message': f"内容审核未通过: {review_result['reason']}"
        }
    
    # 2. 上传图片（如果使用浏览器方案，会在发布时自动上传）
    if isinstance(publisher, XiaohongshuAPIPublisher):
        uploaded_images = []
        for image_path in images:
            try:
                image_url = publisher.upload_image(image_path)
                uploaded_images.append(image_url)
            except Exception as e:
                return {
                    'success': False,
                    'message': f"图片上传失败: {e}"
                }
        images = uploaded_images
    
    # 3. 发布笔记
    try:
        result = publisher.publish_note(
            title=note['title'],
            content=note['content'],
            images=images,
            tags=note['tags']
        )
        
        if result['success']:
            # 记录发布日志
            log_publish_success(note, result['note_id'])
        
        return result
    
    except Exception as e:
        return {
            'success': False,
            'message': f"发布异常: {e}"
        }
```

---

## Step 4: 数据分析

### 4.1 数据采集

**关键指标**：
- 粉丝增长
- 内容互动（点赞、评论、收藏、转发）
- 内容曝光
- 用户画像

**实现代码**：

```python
class XiaohongshuAnalytics:
    def __init__(self, cookies):
        self.cookies = cookies
        self.session = requests.Session()
        # 配置session...
    
    def get_account_stats(self):
        """
        获取账号统计数据
        """
        url = "https://creator.xiaohongshu.com/api/user/stats"
        response = self.session.get(url)
        
        if response.status_code == 200:
            data = response.json()
            return {
                'followers': data['data']['fans'],
                'following': data['data']['follows'],
                'notes': data['data']['notes'],
                'likes': data['data']['likes']
            }
        else:
            raise Exception(f"获取数据失败: {response.text}")
    
    def get_note_stats(self, note_id):
        """
        获取笔记统计数据
        """
        url = f"https://creator.xiaohongshu.com/api/note/{note_id}/stats"
        response = self.session.get(url)
        
        if response.status_code == 200:
            data = response.json()
            return {
                'views': data['data']['views'],
                'likes': data['data']['likes'],
                'comments': data['data']['comments'],
                'collects': data['data']['collects'],
                'shares': data['data']['shares']
            }
        else:
            raise Exception(f"获取数据失败: {response.text}")
    
    def get_all_notes_stats(self, limit=100):
        """
        获取所有笔记统计数据
        """
        url = f"https://creator.xiaohongshu.com/api/user/notes?limit={limit}"
        response = self.session.get(url)
        
        if response.status_code == 200:
            data = response.json()
            notes = data['data']['notes']
            
            stats = []
            for note in notes:
                note_stats = self.get_note_stats(note['id'])
                stats.append({
                    'note_id': note['id'],
                    'title': note['title'],
                    'publish_time': note['time'],
                    **note_stats
                })
            
            return stats
        else:
            raise Exception(f"获取数据失败: {response.text}")
```

---

### 4.2 数据存储

**数据库设计**：

```sql
-- 账号统计表
CREATE TABLE account_stats (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    followers INTEGER,
    following INTEGER,
    notes INTEGER,
    likes INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 笔记统计表
CREATE TABLE note_stats (
    id SERIAL PRIMARY KEY,
    note_id VARCHAR(50) NOT NULL,
    title VARCHAR(200),
    publish_time TIMESTAMP,
    views INTEGER,
    likes INTEGER,
    comments INTEGER,
    collects INTEGER,
    shares INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 每日统计快照
CREATE TABLE daily_stats (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    total_followers INTEGER,
    total_views INTEGER,
    total_likes INTEGER,
    avg_engagement_rate FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**数据采集定时任务**：

```python
import schedule
import time

def collect_daily_stats():
    """
    每日数据采集
    """
    analytics = XiaohongshuAnalytics(cookies)
    
    # 获取账号统计
    account_stats = analytics.get_account_stats()
    save_account_stats(account_stats)
    
    # 获取所有笔记统计
    notes_stats = analytics.get_all_notes_stats()
    save_notes_stats(notes_stats)
    
    # 计算每日汇总
    daily_summary = calculate_daily_summary(notes_stats)
    save_daily_summary(daily_summary)
    
    print(f"数据采集完成: {time.strftime('%Y-%m-%d %H:%M:%S')}")

# 设置定时任务
schedule.every().day.at("23:00").do(collect_daily_stats)

# 运行
while True:
    schedule.run_pending()
    time.sleep(60)
```

---

### 4.3 数据分析

**分析维度**：

1. **增长趋势分析**
   - 粉丝增长曲线
   - 互动量变化
   - 内容表现对比

2. **内容效果分析**
   - 爆款内容特征
   - 最佳发布时间
   - 热门标签

3. **用户画像分析**
   - 活跃时段
   - 兴趣偏好
   - 互动行为

**实现代码**：

```python
import pandas as pd
import matplotlib.pyplot as plt

def analyze_growth_trend(days=30):
    """
    分析增长趋势
    """
    # 读取数据
    df = pd.read_sql("""
        SELECT date, followers, total_views, total_likes
        FROM daily_stats
        WHERE date >= CURRENT_DATE - INTERVAL '%s days'
        ORDER BY date
    """, conn, params=[days])
    
    # 绘制增长曲线
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    
    # 粉丝增长
    axes[0].plot(df['date'], df['followers'], marker='o')
    axes[0].set_title('粉丝增长趋势')
    axes[0].set_ylabel('粉丝数')
    
    # 曝光量
    axes[1].plot(df['date'], df['total_views'], marker='s', color='orange')
    axes[1].set_title('内容曝光趋势')
    axes[1].set_ylabel('曝光量')
    
    # 互动量
    axes[2].plot(df['date'], df['total_likes'], marker='^', color='green')
    axes[2].set_title('互动量趋势')
    axes[2].set_ylabel('点赞数')
    
    plt.tight_layout()
    plt.savefig('reports/growth_trend.png')
    
    return df

def analyze_best_publish_time():
    """
    分析最佳发布时间
    """
    df = pd.read_sql("""
        SELECT 
            EXTRACT(HOUR FROM publish_time) as hour,
            COUNT(*) as note_count,
            AVG(likes + comments + collects) as avg_engagement
        FROM note_stats
        GROUP BY hour
        ORDER BY avg_engagement DESC
    """, conn)
    
    # 可视化
    plt.figure(figsize=(10, 6))
    plt.bar(df['hour'], df['avg_engagement'])
    plt.xlabel('发布时间（小时）')
    plt.ylabel('平均互动量')
    plt.title('最佳发布时间分析')
    plt.savefig('reports/best_publish_time.png')
    
    return df
```

---

## Step 5: 自动化运营

### 5.1 Skills配置

**Skill示例 - 内容生成Skill**：

```yaml
# config/skills/content-generator.yaml
name: content-generator
description: AI内容生成技能
version: 1.0.0

triggers:
  - pattern: "生成内容|内容生成|写笔记"
  - pattern: "生成选题|选题"

actions:
  - name: generate_topic
    description: 生成选题
    parameters:
      - name: interests
        type: array
        description: 用户兴趣列表
      - name: hot_topics
        type: array
        description: 当前热点列表
    
  - name: generate_note
    description: 生成笔记
    parameters:
      - name: topic
        type: string
        description: 选题
      - name: style
        type: string
        enum: [professional_casual, fun_energetic, serious_educational]
        default: professional_casual
```

---

### 5.2 Cron配置

**定时任务配置**：

```yaml
# config/crons/daily-operations.yaml
crontab:
  # 每日选题生成（上午9:00）
  - name: daily-topics
    schedule: "0 9 * * *"
    command: "python scripts/generate_topics.py"
    description: "生成今日选题"
    
  # 自动发布（中午12:00）
  - name: auto-publish
    schedule: "0 12 * * *"
    command: "python scripts/publish_note.py"
    description: "自动发布笔记"
    
  # 互动管理（下午15:00）
  - name: interaction
    schedule: "0 15 * * *"
    command: "python scripts/manage_interaction.py"
    description: "管理评论和私信"
    
  # 数据采集（晚上23:00）
  - name: data-collection
    schedule: "0 23 * * *"
    command: "python scripts/collect_data.py"
    description: "采集每日数据"
    
  # 数据报告（晚上20:00）
  - name: daily-report
    schedule: "0 20 * * *"
    command: "python scripts/send_report.py"
    description: "发送每日报告"
```

---

### 5.3 Rules配置

**规则配置**：

```yaml
# config/rules/operation-rules.yaml
rules:
  # 内容审核规则
  - name: content-review
    trigger: before_publish
    conditions:
      - field: content
        operator: contains_sensitive_words
        value: false
      - field: originality_score
        operator: greater_than
        value: 0.8
    action:
      type: approve
      message: "内容审核通过"
    fallback:
      type: reject
      message: "内容审核未通过"
      notify: true
  
  # 频率限制规则
  - name: rate-limit
    trigger: after_action
    conditions:
      - field: action_type
        operator: equals
        value: publish
      - field: hourly_count
        operator: less_than
        value: 3
    action:
      type: proceed
    fallback:
      type: delay
      duration: 3600
      message: "操作过于频繁，延迟执行"
  
  # 异常处理规则
  - name: error-handling
    trigger: on_error
    conditions:
      - field: error_count
        operator: less_than
        value: 3
    action:
      type: retry
      delay: 300
    fallback:
      type: notify
      message: "操作失败，已超过最大重试次数"
      channel: infoflow
  
  # 工作时间规则
  - name: work-hours
    trigger: before_task
    conditions:
      - field: current_hour
        operator: between
        value: [9, 22]
    action:
      type: proceed
    fallback:
      type: schedule
      time: "09:00"
      message: "非工作时间，已安排到次日执行"
```

---

### 5.4 监控告警

**监控指标**：

```python
# 监控配置
MONITORING_METRICS = {
    # 发布成功率
    'publish_success_rate': {
        'threshold': 0.9,
        'alert': '发布成功率低于90%'
    },
    
    # Cookie有效性
    'cookie_valid': {
        'threshold': True,
        'alert': 'Cookie已过期'
    },
    
    # 粉丝增长
    'follower_growth_rate': {
        'threshold': 0.01,  # 日增长1%
        'alert': '粉丝增长低于预期'
    },
    
    # 互动率
    'engagement_rate': {
        'threshold': 0.05,  # 5%
        'alert': '互动率低于5%'
    }
}

def check_metrics():
    """
    检查监控指标
    """
    alerts = []
    
    # 检查发布成功率
    publish_success_rate = get_publish_success_rate()
    if publish_success_rate < MONITORING_METRICS['publish_success_rate']['threshold']:
        alerts.append(MONITORING_METRICS['publish_success_rate']['alert'])
    
    # 检查Cookie有效性
    cookie_valid = validate_cookies()
    if not cookie_valid:
        alerts.append(MONITORING_METRICS['cookie_valid']['alert'])
    
    # 发送告警
    if alerts:
        send_alert(alerts)
    
    return alerts
```

---

## 总结

以上是完整的实施步骤，从账号准备到自动化运营的全流程。关键点：

1. **Cookie认证** - 解决无GUI问题
2. **内容生成** - AI驱动的创作
3. **平台发布** - 多种方案适配
4. **数据分析** - 数据驱动决策
5. **自动化运营** - 定时任务与规则

接下来可以：
- 按步骤实施
- 根据实际情况调整
- 持续优化迭代

---

_本文档持续更新中..._
