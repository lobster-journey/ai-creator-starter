# 故障排查指南

## 常见问题及解决方案

### 问题1：502 Bad Gateway

**现象**：
- 浏览器访问显示"502 Bad Gateway"
- 页面无法加载

**原因**：
- HTTP服务器未运行
- 服务器进程异常退出
- 端口被其他程序占用

**解决步骤**：

```bash
# 1. 检查服务器状态
ps aux | grep "utf8_file_server"

# 2. 如果未运行，启动服务器
bash ~/.openclaw/skills/sandbox-file-sharing/scripts/start_server.sh

# 3. 如果端口被占用，清理端口
lsof -ti:8194 | xargs kill -9
bash ~/.openclaw/skills/sandbox-file-sharing/scripts/start_server.sh

# 4. 检查日志
tail -50 /tmp/file_server.log
```

---

### 问题2：Empty reply from server

**现象**：
- curl测试返回"Empty reply from server"
- 浏览器显示连接被重置

**原因**：
- 端口被占用但服务未正常运行
- 防火墙阻止连接

**解决步骤**：

```bash
# 1. 查找占用端口的进程
lsof -i:8194

# 2. 强制终止
lsof -ti:8194 | xargs kill -9

# 3. 等待端口释放
sleep 2

# 4. 重启服务器
bash ~/.openclaw/skills/sandbox-file-sharing/scripts/start_server.sh
```

---

### 问题3：文件访问404

**现象**：
- 访问文件显示"404 Not Found"
- 文件明明存在但无法访问

**原因**：
- 文件不在服务目录下
- 文件路径错误
- 文件权限问题

**解决步骤**：

```bash
# 1. 确认服务目录
echo "服务目录: ~/.openclaw/workspace/"

# 2. 检查文件是否存在
ls -la ~/.openclaw/workspace/文件路径

# 3. 如果文件在其他位置，复制到服务目录
cp /path/to/file ~/.openclaw/workspace/

# 4. 检查文件权限
chmod 644 ~/.openclaw/workspace/文件名
```

---

### 问题4：中文乱码

**现象**：
- 浏览器显示中文为乱码
- 文件内容无法正常阅读

**原因**：
- 浏览器未自动识别UTF-8编码
- HTTP响应头未正确设置

**解决方案**：

**方案1：浏览器设置**
- Chrome: 右键 → 编码 → UTF-8
- Firefox: 查看 → 文字编码 → UTF-8

**方案2：下载后查看**
```bash
# 直接下载文件
curl -O https://${PORT}-${SANDBOX_ID}.agent-sandbox.${ENTERPRISE_DOMAIN}/file.md

# 用编辑器打开
vim file.md
# 或
code file.md
```

**方案3：验证响应头**
```bash
curl -I https://${PORT}-${SANDBOX_ID}.agent-sandbox.${ENTERPRISE_DOMAIN}/file.md
# 应该看到: Content-Type: text/markdown; charset=utf-8
```

---

### 问题5：无法访问子目录文件

**现象**：
- 根目录文件可以访问
- 子目录文件返回404

**原因**：
- 文件路径错误
- 目录权限问题

**解决步骤**：

```bash
# 1. 检查目录结构
ls -la ~/.openclaw/workspace/scripts/

# 2. 检查目录权限
ls -ld ~/.openclaw/workspace/scripts/

# 3. 确保目录可读可执行
chmod 755 ~/.openclaw/workspace/scripts/

# 4. 测试访问
curl -I http://localhost:8194/scripts/file.py
```

---

### 问题6：服务器启动失败

**现象**：
- 执行启动脚本失败
- 提示端口已被占用

**原因**：
- 上次服务未正常停止
- 其他程序占用了8194端口

**解决步骤**：

```bash
# 1. 查找所有占用8194端口的进程
lsof -i:8194

# 2. 强制终止所有占用进程
lsof -ti:8194 | xargs kill -9

# 3. 清理PID文件
rm -f /tmp/file_server.pid

# 4. 等待端口释放
sleep 2

# 5. 重新启动
bash ~/.openclaw/skills/sandbox-file-sharing/scripts/start_server.sh
```

---

### 问题7：外部访问失败

**现象**：
- 本地访问正常（localhost:8194）
- 外部访问失败（${PORT}-${SANDBOX_ID}...）

**原因**：
- 网络代理问题
- 防火墙限制
- 服务未监听所有网卡

**解决步骤**：

```bash
# 1. 检查服务监听地址
netstat -tlnp | grep 8194
# 应该看到: 0.0.0.0:8194 (监听所有网卡)

# 2. 测试本地访问
curl -I http://localhost:8194/

# 3. 测试外部访问
curl -I https://${PORT}-${SANDBOX_ID}.agent-sandbox.${ENTERPRISE_DOMAIN}/

# 4. 如果外部访问502，检查日志
tail -100 /tmp/file_server.log
```

---

## 诊断工具

### 快速诊断脚本

```bash
#!/bin/bash
echo "=== 沙箱文件分享服务诊断 ==="
echo ""

# 1. 检查进程
echo "1. 检查进程:"
ps aux | grep "utf8_file_server" | grep -v grep || echo "   ❌ 服务未运行"

# 2. 检查端口
echo ""
echo "2. 检查端口:"
netstat -tlnp 2>/dev/null | grep 8194 || ss -tlnp 2>/dev/null | grep 8194 || echo "   ❌ 端口未监听"

# 3. 检查PID文件
echo ""
echo "3. 检查PID文件:"
if [ -f /tmp/file_server.pid ]; then
  PID=$(cat /tmp/file_server.pid)
  echo "   PID: $PID"
  ps -p $PID > /dev/null 2>&1 && echo "   ✅ 进程存在" || echo "   ❌ 进程不存在"
else
  echo "   ❌ PID文件不存在"
fi

# 4. 测试本地访问
echo ""
echo "4. 测试本地访问:"
curl -s -o /dev/null -w "   HTTP状态: %{http_code}\n" http://localhost:8194/ 2>/dev/null || echo "   ❌ 无法连接"

# 5. 测试外部访问
echo ""
echo "5. 测试外部访问:"
curl -s -o /dev/null -w "   HTTP状态: %{http_code}\n" https://${PORT}-${SANDBOX_ID}.agent-sandbox.${ENTERPRISE_DOMAIN}/ 2>/dev/null || echo "   ❌ 无法连接"

# 6. 检查日志
echo ""
echo "6. 最近日志:"
tail -10 /tmp/file_server.log 2>/dev/null || echo "   ❌ 日志文件不存在"

echo ""
echo "=== 诊断完成 ==="
```

---

## 联系支持

如果以上方法都无法解决问题，请：

1. 收集诊断信息：
```bash
# 保存诊断信息
bash diagnostic.sh > /tmp/diagnostic.txt
```

2. 查看完整日志：
```bash
cat /tmp/file_server.log
```

3. 提供给开发团队分析
