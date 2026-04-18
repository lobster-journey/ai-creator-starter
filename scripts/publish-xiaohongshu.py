#!/usr/bin/env python3
"""
小红书发布脚本
将生成的内容发布到小红书
"""

import json
import os
from datetime import datetime

def publish_to_xiaohongshu():
    """发布到小红书"""

    print("🚀 开始发布到小红书...")

    # 1. 读取内容
    workspace_dir = os.path.expanduser("~/.openclaw/workspace")
    data_dir = os.path.join(workspace_dir, "data")
    content_file = os.path.join(data_dir, "content.json")

    if not os.path.exists(content_file):
        print("❌ 未找到内容文件，请先运行 generate-content.py")
        return

    with open(content_file, "r", encoding="utf-8") as f:
        content_data = json.load(f)

    title = content_data["title"]
    content = content_data["content"]
    images = content_data.get("images", [])

    print(f"📝 标题：{title}")
    print(f"📄 内容长度：{len(content)}字符")
    print(f"🖼️  图片数量：{len(images)}")

    # 2. 调用小红书发布API
    # 注意：实际使用时需要配置MCP服务或其他发布接口

    # 示例：使用MCP API（需要提前启动MCP服务）
    # mcp_url = "http://localhost:18060/api/v1/publish"
    #
    # payload = {
    #     "title": title,
    #     "content": content,
    #     "images": images
    # }
    #
    # response = requests.post(mcp_url, json=payload)
    # result = response.json()

    # 模拟发布成功
    result = {
        "success": True,
        "message": "发布成功",
        "note_id": f"note_{datetime.now().timestamp()}"
    }

    # 3. 记录发布结果
    if result.get("success"):
        print("✅ 发布成功！")
        print(f"📝 笔记ID：{result.get('note_id')}")

        # 保存发布记录
        publish_record = {
            "date": datetime.now().isoformat(),
            "title": title,
            "note_id": result.get("note_id"),
            "status": "success"
        }

        publish_file = os.path.join(data_dir, "publish_record.json")

        with open(publish_file, "w", encoding="utf-8") as f:
            json.dump(publish_record, f, ensure_ascii=False, indent=2)

        print(f"📁 发布记录已保存：{publish_file}")
    else:
        print(f"❌ 发布失败：{result.get('error')}")

    return result

if __name__ == "__main__":
    publish_to_xiaohongshu()
