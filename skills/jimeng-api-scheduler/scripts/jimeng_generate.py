#!/usr/bin/env python3
"""
即梦API图片生成工具
快速调用即梦AI生成图片
"""
import requests
import sys
import os
from pathlib import Path

# 配置文件路径
CONFIG_FILE = Path.home() / '.openclaw' / 'workspace' / 'config' / 'jimeng' / 'config.env'

def load_config():
    """加载配置"""
    config = {}
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    return config

def generate_image(prompt, ratio='16:9', resolution='2k', model='jimeng-4.5'):
    """生成图片"""
    config = load_config()
    
    api_url = config.get('JIMENG_API_URL', 'http://localhost:5100')
    session_id = config.get('JIMENG_SESSION_ID')
    
    if not session_id:
        print("❌ 未找到Session ID，请先配置")
        return None
    
    print(f"🎨 正在生成图片...")
    print(f"   提示词: {prompt}")
    print(f"   比例: {ratio}, 分辨率: {resolution}")
    
    try:
        response = requests.post(
            f'{api_url}/v1/images/generations',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {session_id}'
            },
            json={
                'model': model,
                'prompt': prompt,
                'ratio': ratio,
                'resolution': resolution
            },
            timeout=90
        )
        
        result = response.json()
        
        if 'data' in result:
            urls = [img['url'] for img in result['data']]
            print(f"\n✅ 成功生成 {len(urls)} 张图片:\n")
            for i, url in enumerate(urls, 1):
                print(f"   图片{i}: {url}\n")
            return urls
        else:
            print(f"❌ 生成失败: {result}")
            return None
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return None

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python jimeng_generate.py <提示词> [比例] [分辨率]")
        print("示例: python jimeng_generate.py '一只可爱的小龙虾' 16:9 2k")
        sys.exit(1)
    
    prompt = sys.argv[1]
    ratio = sys.argv[2] if len(sys.argv) > 2 else '16:9'
    resolution = sys.argv[3] if len(sys.argv) > 3 else '2k'
    
    generate_image(prompt, ratio, resolution)

if __name__ == '__main__':
    main()
