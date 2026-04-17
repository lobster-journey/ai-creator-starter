# 🔐 账号安全

> 账号保护与安全措施

---

## 🔑 认证安全

### Cookie管理

**Cookie存储**：
- 加密存储
- 本地存储
- 定期更新

**Cookie保护**：
- 不分享给他人
- 不上传到公开仓库
- 定期检查有效性

---

### API密钥管理

**密钥存储**：
```bash
# 使用环境变量
export CLAUDE_API_KEY="your_key"

# 使用加密文件
python tools/encrypt_key.py
```

**密钥保护**：
- 不硬编码在代码中
- 不提交到Git仓库
- 定期更换密钥

---

## 🛡️ 防封策略

### 频率控制

**发布频率**：
- 小红书：2-3篇/天
- 抖音：1-2条/天
- B站：1条/天

**间隔控制**：
- 最小间隔30分钟
- 随机延迟5-10分钟
- 避免固定模式

---

### 行为模拟

**真实用户行为**：
```python
class UserBehaviorSimulator:
    async def simulate(self):
        # 随机浏览
        await self.random_browse()

        # 随机互动
        await self.random_interact()

        # 随机停留
        await self.random_stay()

        # 执行操作
        await self.execute_action()
```

---

## 🚨 异常监控

### 监控指标

1. **账号状态**
   - 登录状态
   - 发布权限
   - 流量限制

2. **操作成功率**
   - 发布成功率
   - 互动成功率
   - 数据采集成功率

---

### 异常告警

```python
class AccountMonitor:
    async def check_account_status(self):
        # 检查登录状态
        if not await self.is_logged_in():
            await self.alert('账号已登出')

        # 检查发布权限
        if not await self.can_publish():
            await self.alert('发布权限受限')

        # 检查流量
        if await self.is_traffic_limited():
            await self.alert('流量受限')
```

---

## 🔄 故障恢复

### Cookie过期

**自动处理**：
1. 检测到Cookie过期
2. 发送通知给用户
3. 等待用户更新Cookie
4. 恢复运营

---

### 账号封禁

**应对措施**：
1. 分析封禁原因
2. 准备申诉材料
3. 提交申诉
4. 调整运营策略

---

## 📊 安全检查清单

### 日常检查

- [ ] Cookie有效期
- [ ] API密钥安全
- [ ] 发布频率合理
- [ ] 无违规内容
- [ ] 无异常登录

---

### 周度检查

- [ ] 账号安全状态
- [ ] 发布成功率统计
- [ ] 风险内容排查
- [ ] 安全策略更新

---

## 📚 相关文档

- [内容合规](./compliance.md)
- [隐私保护](./privacy.md)
- [自动化运营](./automation.md)

---

**Created by 🦞 Lobster Journey Studio**
