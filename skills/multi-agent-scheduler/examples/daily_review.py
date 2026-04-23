"""
每日复盘流程示例
展示如何使用调度引擎执行每日复盘任务
"""

import asyncio
import sys
sys.path.append('..')

from scheduler.engine import SchedulerEngine, AgentTask


async def main():
    """执行每日复盘流程"""
    
    # 创建调度引擎
    scheduler = SchedulerEngine()
    
    # 定义复盘任务
    review_task = AgentTask(
        agent_id="agent-reviewer",
        task_name="每日工作复盘",
        task_description="""
        执行每日工作复盘：
        1. 收集今日所有工作记录
        2. 分析工作成果和问题
        3. 提炼学习心得和技术突破
        4. 生成结构化的图文日报
        5. 发送给用户
        """,
        timeout_seconds=1200  # 20分钟
    )
    
    # 执行复盘任务
    print("="*60)
    print("🌙 开始执行每日工作复盘")
    print("="*60)
    
    result = await scheduler.spawn_agent(review_task)
    
    # 输出结果
    print("\n" + "="*60)
    print("📊 执行结果")
    print("="*60)
    print(f"成功: {result.success}")
    print(f"执行时长: {result.duration_seconds:.1f}秒")
    if result.error:
        print(f"错误: {result.error}")
    else:
        print(f"复盘内容: {result.result[:200]}...")


if __name__ == "__main__":
    asyncio.run(main())
