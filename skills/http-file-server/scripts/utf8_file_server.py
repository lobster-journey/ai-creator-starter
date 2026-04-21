#!/usr/bin/env python3
"""
沙箱文件分享 - UTF-8强制编码HTTP服务器
端口: 8194
服务目录: ~/.openclaw/workspace/
"""
import http.server
import socketserver
import os
import mimetypes

PORT = 8194
DIRECTORY = os.path.expanduser("~/.openclaw/workspace")

# 配置mimetypes添加UTF-8编码
mimetypes.init()
mimetypes.add_type('text/markdown; charset=utf-8', '.md')
mimetypes.add_type('text/plain; charset=utf-8', '.txt')
mimetypes.add_type('text/html; charset=utf-8', '.html')
mimetypes.add_type('text/css; charset=utf-8', '.css')
mimetypes.add_type('text/javascript; charset=utf-8', '.js')
mimetypes.add_type('application/json; charset=utf-8', '.json')
mimetypes.add_type('application/xml; charset=utf-8', '.xml')
mimetypes.add_type('text/x-python; charset=utf-8', '.py')
mimetypes.add_type('text/x-java-source; charset=utf-8', '.java')
mimetypes.add_type('text/x-go; charset=utf-8', '.go')
mimetypes.add_type('text/x-c; charset=utf-8', '.c')
mimetypes.add_type('text/x-c++; charset=utf-8', '.cpp')
mimetypes.add_type('text/csv; charset=utf-8', '.csv')
mimetypes.add_type('application/x-yaml; charset=utf-8', '.yaml')
mimetypes.add_type('application/x-yaml; charset=utf-8', '.yml')

class UTF8Handler(http.server.SimpleHTTPRequestHandler):
    """强制UTF-8编码的HTTP请求处理器"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        """在响应头中强制添加UTF-8编码"""
        content_type = self.headers.get('Content-Type', '')
        
        # 如果是文本类型但没有charset，添加charset=utf-8
        if content_type and 'text/' in content_type and 'charset' not in content_type:
            # 移除旧的Content-Type
            if 'Content-Type' in self.headers:
                del self.headers['Content-Type']
            self.send_header('Content-Type', content_type + '; charset=utf-8')
        
        super().end_headers()
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{self.address_string()}] {format % args}")

if __name__ == "__main__":
    try:
        with socketserver.TCPServer(("", PORT), UTF8Handler) as httpd:
            print("=" * 60)
            print("🦞 沙箱文件分享服务器")
            print("=" * 60)
            print(f"✅ 服务器运行中")
            print(f"   端口: {PORT}")
            print(f"   服务目录: {DIRECTORY}")
            print(f"   编码: UTF-8（强制）")
            print(f"   访问格式: https://{PORT}-u9f5u8ji.agent-sandbox.baidu-int.com/文件路径")
            print("=" * 60)
            print()
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"错误: {e}")
        raise
