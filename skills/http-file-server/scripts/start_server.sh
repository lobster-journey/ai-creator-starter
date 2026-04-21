#!/bin/bash
# 沙箱文件分享 - HTTP服务器启动脚本
# 端口: 8194
# 服务目录: ~/.openclaw/workspace/

PORT=8194
WORK_DIR="$HOME/.openclaw/workspace"
SKILL_DIR="$HOME/.openclaw/skills/http-file-server"
PID_FILE="/tmp/file_server.pid"
LOG_FILE="/tmp/file_server.log"

echo "=== 沙箱文件分享服务器 ==="
echo ""

# 检查是否已运行
if [ -f "$PID_FILE" ]; then
  PID=$(cat "$PID_FILE")
  if ps -p $PID > /dev/null 2>&1; then
    echo "✅ 服务器已在运行"
    echo "   PID: $PID"
    echo "   端口: $PORT"
    echo ""
    echo "访问地址格式:"
    echo "   https://${PORT}-u9f5u8ji.agent-sandbox.baidu-int.com/文件路径"
    exit 0
  fi
fi

# 清理端口
echo "清理端口 $PORT..."
lsof -ti:$PORT | xargs kill -9 2>/dev/null
sleep 1

# 启动UTF-8服务器
echo "启动UTF-8文件服务器..."
nohup python3 "$SKILL_DIR/scripts/utf8_file_server.py" > "$LOG_FILE" 2>&1 &
PID=$!

# 保存PID
echo $PID > "$PID_FILE"

sleep 2

# 验证服务
if ps -p $PID > /dev/null 2>&1; then
  echo ""
  echo "✅ 服务器启动成功"
  echo "   PID: $PID"
  echo "   端口: $PORT"
  echo "   服务目录: $WORK_DIR"
  echo "   日志文件: $LOG_FILE"
  echo "   编码: UTF-8（强制）"
  echo ""
  echo "=== 访问地址格式 ==="
  echo "https://${PORT}-u9f5u8ji.agent-sandbox.baidu-int.com/文件路径"
  echo ""
  echo "=== 示例 ==="
  echo "📄 MEMORY.md"
  echo "   https://${PORT}-u9f5u8ji.agent-sandbox.baidu-int.com/MEMORY.md"
  echo ""
  echo "💻 scripts/jimeng_generate.py"
  echo "   https://${PORT}-u9f5u8ji.agent-sandbox.baidu-int.com/scripts/jimeng_generate.py"
else
  echo "❌ 服务器启动失败"
  echo "查看日志: tail -50 $LOG_FILE"
  exit 1
fi
