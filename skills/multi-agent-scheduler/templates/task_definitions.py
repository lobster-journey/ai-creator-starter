"""
任务定义模块
定义所有定时任务的Agent分配和执行逻辑
"""

from dataclasses import dataclass
from typing import List, Dict, Any
from enum import Enum


class TaskPriority(Enum):
    """任务优先级"""
    HIGH = 1      # 高优先级：内容生产、公司调研
    MEDIUM = 2    # 中优先级：数据简报、竞品追踪
    LOW = 3       # 低优先级：系统检查、备份


@dataclass
class TaskDefinition:
    """任务定义"""
    task_id: str
    task_name: str
    cron_expr: str
    agent_id: str
    task_description: str
    timeout_seconds: int
    priority: TaskPriority
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


# 定时任务定义
TASK_DEFINITIONS = {
    # 内容生产类（高优先级）
    "content_production": TaskDefinition(
        task_id="content_production",
        task_name="每日内容生产",
        cron_expr="0 8 * * *",
        agent_id="agent-main",  # 总经理调度
        task_description="执行完整的内容生产流程：热点侦察 → 文案创作+配图 → 质检",
        timeout_seconds=3600,  # 1小时
        priority=TaskPriority.HIGH
    ),
    
    # 工具维护类（中优先级）
    "jimeng_credit": TaskDefinition(
        task_id="jimeng_credit",
        task_name="即梦每日积分获取",
        cron_expr="0 9 * * *",
        agent_id="agent-jimeng-credit",
        task_description="每日访问即梦网站，获取60积分奖励",
        timeout_seconds=300,  # 5分钟
        priority=TaskPriority.MEDIUM
    ),
    
    # 监测类（中优先级）
    "hot_spot_scan": TaskDefinition(
        task_id="hot_spot_scan",
        task_name="热点快速扫描",
        cron_expr="0 10 * * *",
        agent_id="agent-hot-scout",
        task_description="快速扫描当日AI/科技热点，输出热点更新简报",
        timeout_seconds=900,  # 15分钟
        priority=TaskPriority.MEDIUM
    ),
    
    "data_report": TaskDefinition(
        task_id="data_report",
        task_name="午间数据简报",
        cron_expr="0 12 * * *",
        agent_id="agent-analyst",
        task_description="统计前一日小红书数据，生成数据简报卡片",
        timeout_seconds=600,  # 10分钟
        priority=TaskPriority.MEDIUM
    ),
    
    "competitor_track": TaskDefinition(
        task_id="competitor_track",
        task_name="竞品动态追踪",
        cron_expr="0 14 * * *",
        agent_id="agent-competitor",
        task_description="检查对标账号最新发布，记录爆款特征",
        timeout_seconds=1200,  # 20分钟
        priority=TaskPriority.MEDIUM
    ),
    
    "content_analysis": TaskDefinition(
        task_id="content_analysis",
        task_name="内容表现分析",
        cron_expr="0 16 * * *",
        agent_id="agent-analyst",
        task_description="分析已有笔记表现数据，提出内容改进建议",
        timeout_seconds=900,  # 15分钟
        priority=TaskPriority.MEDIUM
    ),
    
    "interaction_check": TaskDefinition(
        task_id="interaction_check",
        task_name="互动数据检查",
        cron_expr="0 18 * * *",
        agent_id="agent-main",
        task_description="检查小红书评论私信数据，汇总互动摘要",
        timeout_seconds=600,  # 10分钟
        priority=TaskPriority.MEDIUM
    ),
    
    "review_prep": TaskDefinition(
        task_id="review_prep",
        task_name="复盘准备工作",
        cron_expr="0 20 * * *",
        agent_id="agent-reviewer",
        task_description="收集今日工作素材，整理数据统计",
        timeout_seconds=900,  # 15分钟
        priority=TaskPriority.MEDIUM
    ),
    
    # 调研类（高优先级）
    "company_research": TaskDefinition(
        task_id="company_research",
        task_name="每日公司调研",
        cron_expr="30 21 * * *",
        agent_id="agent-main",  # 总经理调度
        task_description="执行公司调研流程：调研员1-5并发 → 洞察提炼师串行",
        timeout_seconds=3600,  # 1小时
        priority=TaskPriority.HIGH
    ),
    
    # 复盘类（高优先级）
    "daily_review": TaskDefinition(
        task_id="daily_review",
        task_name="每晚工作复盘",
        cron_expr="0 22 * * *",
        agent_id="agent-reviewer",
        task_description="每日工作复盘，生成图文日报",
        timeout_seconds=1200,  # 20分钟
        priority=TaskPriority.HIGH
    ),
    
    # 系统维护类（低优先级）
    "system_check": TaskDefinition(
        task_id="system_check",
        task_name="系统健康检查",
        cron_expr="0 23 * * *",
        agent_id="agent-main",
        task_description="检查Gateway、API、Skills状态，清理临时文件",
        timeout_seconds=600,  # 10分钟
        priority=TaskPriority.LOW
    ),
}


def get_task_by_time(hour: int, minute: int = 0) -> List[TaskDefinition]:
    """根据时间获取要执行的任务"""
    cron_expr = f"{minute} {hour} * * *"
    return [task for task in TASK_DEFINITIONS.values() if task.cron_expr == cron_expr]


def get_all_tasks() -> Dict[str, TaskDefinition]:
    """获取所有任务定义"""
    return TASK_DEFINITIONS


def get_tasks_by_priority(priority: TaskPriority) -> List[TaskDefinition]:
    """根据优先级获取任务"""
    return [task for task in TASK_DEFINITIONS.values() if task.priority == priority]
