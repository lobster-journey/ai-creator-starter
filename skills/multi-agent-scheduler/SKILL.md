# Multi-Agent Scheduler Skill

多Agent调度引擎，用于龙虾巡游记公司的自动化运营。

## 功能特性

- ✅ **串行任务调度**：按顺序执行任务，等待前一个完成
- ✅ **并发任务调度**：同时启动多个Agent，提升效率
- ✅ **质量检查与返工**：最多5次返工，确保输出质量
- ✅ **超时保护**：每个任务15分钟超时，自动终止
- ✅ **错误处理**：单个Agent失败不影响整体流程
- ✅ **任务依赖管理**：支持任务间的依赖关系

## 支持的Agent

### 总经办 HQ
- 总经理🦞 (agent-main) - 战略决策、任务调度
- 复盘官📝 (agent-reviewer) - 每日工作复盘

### 内容生产部 Content Dept
- 热点侦察员🔍 (agent-hot-scout) - 热点搜索与选题
- 文案创作员✍️ (agent-copywriter) - 内容创作
- 质检员🔎 (agent-qa) - 质量检查
- 配图师🎨 (agent-designer) - 配图生成

### 调研部 Research Dept
- 调研员🔬 (agent-researcher-[1-5]) - 公司深度调研
- 洞察提炼师💡 (agent-insight) - 跨公司洞察提炼

### 运营部 Operation Dept
- 数据分析师📊 (agent-analyst) - 数据追踪与分析
- 竞品监察员👁️ (agent-competitor) - 竞品动态追踪

## 核心调度模式

### 1. 内容生产流程
```
阶段1（串行）：热点侦察员 → 输出选题报告
阶段2（并发）：文案创作员 + 配图师（同时执行）
阶段3（串行）：质检员 → 通过/返工（最多5次）
```

### 2. 公司调研流程
```
阶段1（并发）：调研员1-5（5人同时调研）
阶段2（串行）：洞察提炼师 → 提炼共性洞察
```

### 3. 每日复盘流程
```
复盘官 → 生成图文日报 → 发送
```

## 使用方法

### 在Skill中使用

```python
# 读取调度引擎
from scheduler.engine import SchedulerEngine

# 创建调度器
scheduler = SchedulerEngine()

# 执行内容生产流程
result = await scheduler.execute_content_production()

# 执行公司调研流程
companies = ["Notion", "Grammarly", "Figma", "ElevenLabs", "Runway"]
result = await scheduler.execute_company_research(companies)
```

### Agent提示词模板

所有Agent的详细提示词模板见：`templates/agent_templates.md`

## 文件结构

```
multi-agent-scheduler/
├── SKILL.md                      # 本文件
├── scheduler/
│   ├── engine.py                 # 调度引擎核心代码
│   └── __init__.py
├── templates/
│   ├── agent_templates.md        # Agent提示词模板
│   ├── company_structure.md      # 组织架构定义
│   └── task_definitions.py       # 任务定义
├── examples/
│   ├── content_production.py     # 内容生产示例
│   ├── company_research.py       # 公司调研示例
│   └── daily_review.py           # 每日复盘示例
└── tests/
    ├── test_engine.py            # 引擎测试
    └── test_agents.py            # Agent测试
```

## 配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| max_retries | 5 | 质检最大返工次数 |
| timeout_seconds | 900 | 单个任务超时时间（15分钟） |
| max_concurrent_agents | 5 | 最大并发Agent数量 |
| error_handling | continue | 错误处理策略 |

## 质量保证

### 5次检查循环（质检员）
1. **完整性检查**：标题、正文、标签是否完整
2. **去AI化检查**：避免AI痕迹，自然流畅
3. **违规风险检查**：确保合规，避免违规
4. **原创性检查**：确保原创，不抄袭洗稿
5. **可读性检查**：分段清晰，易于阅读

### 返工机制
- 不合格明确指出问题
- 提供具体修改建议
- 最多返工5次
- 第6次选最优版本交付

## 性能优化

- **并发执行**：文案+配图并发，调研员5人并发，效率提升50%+
- **超时保护**：避免单个任务阻塞整体流程
- **错误隔离**：单个Agent失败不影响其他Agent

## 扩展性

### 添加新Agent
1. 在 `templates/agent_templates.md` 添加提示词模板
2. 在 `scheduler/engine.py` 添加调度逻辑
3. 在 `examples/` 添加使用示例

### 添加新流程
1. 在 `scheduler/engine.py` 添加新的执行方法
2. 定义任务依赖关系
3. 配置并发/串行模式

## 监控与日志

所有任务执行结果自动记录，包括：
- 执行时间
- 成功/失败状态
- 错误信息
- 质量评分

## 维护者

龙虾巡游记公司 - 总经理🦞

## 版本历史

- v1.0 (2026-04-23) - 初始版本，支持11个定时任务
