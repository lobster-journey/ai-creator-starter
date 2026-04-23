#!/usr/bin/env python3
"""
官网内容和图片爬虫（带智能筛选）
用于获取官网高质量内容和图片，自动筛选适合小红书的内容
"""

import os
import json
import time
import hashlib
import requests
from pathlib import Path
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import argparse
import re


class ContentFilter:
    """内容筛选器"""

    def __init__(self):
        # 小红书适合的关键词
        self.good_keywords = [
            'AI', '人工智能', '大模型', 'GPT', 'Claude', 'OpenAI',
            '工具', '技巧', '教程', '指南', '方法', '实战',
            '新功能', '更新', '发布', '推出',
            '提升', '优化', '效率', '生产力',
            '免费', '开源', '资源', '模板'
        ]

        # 不适合的关键词
        self.bad_keywords = [
            '投资者', '股价', '财报', '股票', '融资',
            '法律', '诉讼', '版权', '侵权',
            '招聘', '求职', '简历',
            '活动', '促销', '优惠', '折扣'
        ]

    def score_content(self, content):
        """
        评分内容是否适合小红书

        Args:
            content: 内容字典

        Returns:
            dict: 评分结果
        """
        score = 0
        reasons = []

        text = content.get('text', '')
        title = content.get('title', '')
        description = content.get('description', '')
        combined_text = f"{title} {description} {text}".lower()

        # 1. 标题长度（小红书标题适合10-20字）
        if 10 <= len(title) <= 30:
            score += 10
            reasons.append("✅ 标题长度适中")
        else:
            reasons.append("⚠️ 标题长度不合适")

        # 2. 内容长度（小红书适合500-2000字）
        text_length = len(text)
        if 300 <= text_length <= 2000:
            score += 15
            reasons.append("✅ 内容长度适中")
        elif 200 <= text_length < 300 or 2000 < text_length <= 3000:
            score += 8
            reasons.append("⚠️ 内容长度可以接受")
        else:
            reasons.append("❌ 内容长度不合适")

        # 3. 好关键词匹配
        good_matches = sum(1 for kw in self.good_keywords if kw.lower() in combined_text)
        score += good_matches * 5
        if good_matches > 0:
            reasons.append(f"✅ 包含{good_matches}个适合关键词")

        # 4. 坏关键词匹配
        bad_matches = sum(1 for kw in self.bad_keywords if kw.lower() in combined_text)
        score -= bad_matches * 10
        if bad_matches > 0:
            reasons.append(f"❌ 包含{bad_matches}个不适合关键词")

        # 5. 图片数量（小红书适合2-6张图）
        image_count = len(content.get('images', []))
        if 2 <= image_count <= 6:
            score += 15
            reasons.append(f"✅ 图片数量适中（{image_count}张）")
        elif image_count > 6:
            score += 5
            reasons.append(f"⚠️ 图片较多（{image_count}张）")
        else:
            reasons.append(f"❌ 图片不足（{image_count}张）")

        # 6. 内容质量
        # 包含数字、列表、代码等实用内容
        if re.search(r'\d+', text):
            score += 5
            reasons.append("✅ 包含数字信息")
        if '•' in text or '-' in text or '1.' in text:
            score += 5
            reasons.append("✅ 包含列表结构")

        # 7. 相关性判断
        # 是否与AI、科技、工具相关
        ai_tech_keywords = ['ai', '人工智能', '科技', '工具', '软件', '应用', '平台']
        if any(kw in combined_text for kw in ai_tech_keywords):
            score += 10
            reasons.append("✅ 与AI/科技相关")

        # 判断是否适合
        is_suitable = score >= 30

        return {
            'score': score,
            'is_suitable': is_suitable,
            'reasons': reasons,
            'recommendation': self._get_recommendation(score)
        }

    def _get_recommendation(self, score):
        """获取推荐意见"""
        if score >= 50:
            return "🌟 强烈推荐"
        elif score >= 40:
            return "✅ 推荐"
        elif score >= 30:
            return "⚠️ 可以考虑"
        elif score >= 20:
            return "❓ 需要修改"
        else:
            return "❌ 不推荐"

    def extract_key_points(self, content):
        """提取关键点"""
        text = content.get('text', '')
        lines = text.split('\n')

        key_points = []
        for line in lines[:20]:  # 只看前20行
            line = line.strip()
            # 提取带数字的行
            if re.match(r'^\d+[\.\、]', line):
                key_points.append(line)
            # 提取带符号的行
            elif line.startswith('•') or line.startswith('-') or line.startswith('•'):
                key_points.append(line)
            # 提取短句（10-50字）
            elif 10 <= len(line) <= 50:
                key_points.append(line)

        return key_points[:5]  # 最多5个关键点


class OfficialSiteCrawler:
    """官网爬虫（带智能筛选）"""

    def __init__(self, output_dir="./output"):
        self.output_dir = Path(output_dir)
        self.images_dir = self.output_dir / "images"
        self.content_dir = self.output_dir / "content"
        self.filtered_dir = self.output_dir / "filtered"

        # 创建目录
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.content_dir.mkdir(parents=True, exist_ok=True)
        self.filtered_dir.mkdir(parents=True, exist_ok=True)

        # 请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        # 会话
        self.session = requests.Session()
        self.session.headers.update(self.headers)

        # 内容筛选器
        self.filter = ContentFilter()

    def crawl_and_filter(self, url, save_images=True, min_score=30):
        """
        爬取并筛选内容

        Args:
            url: 页面URL
            save_images: 是否保存图片
            min_score: 最低分数阈值

        Returns:
            dict: 筛选后的内容
        """
        print(f"\n{'='*60}")
        print(f"🔍 正在爬取: {url}")
        print(f"{'='*60}\n")

        # 爬取内容
        content = self._crawl_page(url, save_images)
        if not content:
            return None

        # 筛选内容
        print(f"\n{'='*60}")
        print(f"📊 正在筛选内容...")
        print(f"{'='*60}\n")

        score_result = self.filter.score_content(content)

        # 显示评分详情
        print(f"标题: {content['title']}")
        print(f"评分: {score_result['score']}分")
        print(f"推荐: {score_result['recommendation']}")
        print(f"\n评分详情:")
        for reason in score_result['reasons']:
            print(f"  {reason}")

        # 提取关键点
        key_points = self.filter.extract_key_points(content)
        if key_points:
            print(f"\n关键点:")
            for i, point in enumerate(key_points, 1):
                print(f"  {i}. {point[:50]}...")

        # 判断是否适合
        if score_result['is_suitable']:
            print(f"\n✅ 内容适合小红书！")
            # 保存筛选结果
            self._save_filtered_content(content, score_result, key_points)
        else:
            print(f"\n❌ 内容不适合小红书")
            print(f"💡 建议: 需要大幅修改或重新选题")

        # 保存原始内容
        self._save_content(content, score_result)

        return {
            'content': content,
            'score': score_result,
            'key_points': key_points
        }

    def _crawl_page(self, url, save_images):
        """爬取页面"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            content = {
                'url': url,
                'title': self._extract_title(soup),
                'description': self._extract_description(soup),
                'text': self._extract_text(soup),
                'images': [],
                'links': [],
                'metadata': self._extract_metadata(soup),
                'crawled_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }

            if save_images:
                images = self._extract_images(soup, url)
                content['images'] = images

            links = self._extract_links(soup, url)
            content['links'] = links[:10]

            return content

        except Exception as e:
            print(f"❌ 爬取失败: {e}")
            return None

    def _extract_title(self, soup):
        """提取标题"""
        title = soup.find('title')
        if title:
            return title.get_text().strip()
        h1 = soup.find('h1')
        if h1:
            return h1.get_text().strip()
        return "无标题"

    def _extract_description(self, soup):
        """提取描述"""
        meta = soup.find('meta', attrs={'name': 'description'})
        if meta and meta.get('content'):
            return meta['content']
        og = soup.find('meta', attrs={'property': 'og:description'})
        if og and og.get('content'):
            return og['content']
        p = soup.find('p')
        if p:
            text = p.get_text().strip()
            return text[:200] if len(text) > 200 else text
        return ""

    def _extract_text(self, soup):
        """提取正文"""
        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text(separator='\n', strip=True)
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return '\n'.join(lines[:100])

    def _extract_images(self, soup, base_url):
        """提取图片"""
        images = []
        img_tags = soup.find_all('img')

        for img in img_tags[:20]:
            src = img.get('src') or img.get('data-src')
            if not src:
                continue

            img_url = urljoin(base_url, src)

            # 过滤
            if any(x in img_url.lower() for x in ['icon', 'logo', 'avatar', 'favicon']):
                continue

            image_info = self._download_image(img_url)
            if image_info:
                images.append(image_info)
                time.sleep(0.3)

        return images

    def _download_image(self, img_url):
        """下载图片"""
        try:
            response = self.session.get(img_url, timeout=15)
            response.raise_for_status()

            ext = os.path.splitext(urlparse(img_url).path)[1] or '.jpg'
            if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                ext = '.jpg'

            filename = hashlib.md5(img_url.encode()).hexdigest() + ext
            filepath = self.images_dir / filename

            # 只保存大于10KB的图片
            if len(response.content) < 10240:
                return None

            with open(filepath, 'wb') as f:
                f.write(response.content)

            return {
                'url': img_url,
                'filename': filename,
                'local_path': str(filepath),
                'size': len(response.content)
            }

        except Exception as e:
            return None

    def _extract_links(self, soup, base_url):
        """提取链接"""
        links = []
        a_tags = soup.find_all('a', href=True)

        for a in a_tags[:20]:
            href = a['href']
            text = a.get_text().strip()
            full_url = urljoin(base_url, href)

            if text and full_url.startswith('http'):
                links.append({
                    'text': text,
                    'url': full_url
                })

        return links

    def _extract_metadata(self, soup):
        """提取元数据"""
        metadata = {}

        og_tags = soup.find_all('meta', attrs={'property': lambda x: x and x.startswith('og:')})
        for tag in og_tags:
            prop = tag.get('property')
            content = tag.get('content')
            if prop and content:
                metadata[prop] = content

        return metadata

    def _save_content(self, content, score_result):
        """保存原始内容"""
        url_hash = hashlib.md5(content['url'].encode()).hexdigest()[:8]
        filename = f"raw_{content['title'][:20]}_{url_hash}.json"
        filename = filename.replace('/', '_').replace('\\', '_')

        filepath = self.content_dir / filename

        data = {
            'content': content,
            'score': score_result
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _save_filtered_content(self, content, score_result, key_points):
        """保存筛选后的内容"""
        url_hash = hashlib.md5(content['url'].encode()).hexdigest()[:8]
        filename = f"filtered_{content['title'][:20]}_{url_hash}.json"
        filename = filename.replace('/', '_').replace('\\', '_')

        filepath = self.filtered_dir / filename

        data = {
            'content': content,
            'score': score_result,
            'key_points': key_points,
            'xiaohongshu_suggestion': {
                'title': content['title'][:20],  # 小红书标题建议
                'images_count': len(content['images']),
                'text_length': len(content['text']),
                'key_points': key_points
            }
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"📄 筛选结果已保存: {filename}")


def main():
    parser = argparse.ArgumentParser(description='官网内容爬虫（带智能筛选）')
    parser.add_argument('url', help='要爬取的URL')
    parser.add_argument('--output', '-o', default='./output', help='输出目录')
    parser.add_argument('--no-images', action='store_true', help='不下载图片')
    parser.add_argument('--min-score', type=int, default=30, help='最低分数阈值')

    args = parser.parse_args()

    crawler = OfficialSiteCrawler(output_dir=args.output)
    result = crawler.crawl_and_filter(
        args.url,
        save_images=not args.no_images,
        min_score=args.min_score
    )

    if result and result['score']['is_suitable']:
        print(f"\n{'='*60}")
        print(f"✅ 爬取完成！内容适合小红书发布")
        print(f"{'='*60}\n")
    else:
        print(f"\n{'='*60}")
        print(f"❌ 爬取完成，但内容不适合小红书")
        print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
