#!/usr/bin/env python3
"""
内容生成脚本
基于热点生成小红书笔记内容
"""

import json
import os
from datetime import datetime

def generate_xiaohongshu_note():
    """生成小红书笔记"""

    print("📝 开始生成小红书笔记...")

    # 1. 读取热点
    workspace_dir = os.path.expanduser("~/.openclaw/workspace")
    data_dir = os.path.join(workspace_dir, "data")
    hotspots_file = os.path.join(data_dir, "hotspots.json")

    if not os.path.exists(hotspots_file):
        print("❌ 未找到热点文件，请先运行 collect-hotspots.py")
        return

    with open(hotspots_file, "r", encoding="utf-8") as f:
        hotspots_data = json.load(f)

    # 2. 选择最热点的主题
    topic = hotspots_data["hotspots"][0]["title"]
    topic_summary = hotspots_data["hotspots"][0]["summary"]

    print(f"🎯 选题：{topic}")

    # 3. 生成内容（实际使用时调用LLM API）
    # 这里提供模板示例

    title = f"🔥 {topic.split('，')[0]}"

    content = f"""{topic}

最近这个话题太火了！作为AI领域的观察者，我来给大家解读一下：

📌 核心要点：
{topic_summary}

💡 我的思考：
这个发展对AI行业意味着什么？未来会带来哪些变化？

🎯 对我们的影响：
- 技术层面：AI能力持续突破
- 应用层面：更多场景将被AI赋能
- 成本层面：AI使用门槛持续降低

✨ 总结：
AI发展速度惊人，我们要保持学习，紧跟趋势！

#AI #人工智能 #科技前沿 #AI工具 #科技资讯
"""

    # 4. 保存内容
    output = {
        "date": datetime.now().isoformat(),
        "topic": topic,
        "title": title,
        "content": content,
        "images": []  # 图片URL列表
    }

    output_file = os.path.join(data_dir, "content.json")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✅ 已生成内容")
    print(f"📁 保存到：{output_file}")
    print(f"\n标题：{title}")
    print(f"\n内容预览：\n{content[:200]}...")

    return output

if __name__ == "__main__":
    generate_xiaohongshu_note()
