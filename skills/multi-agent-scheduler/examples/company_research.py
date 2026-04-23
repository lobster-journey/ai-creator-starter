"""
公司调研流程示例
展示如何使用调度引擎执行公司调研任务
"""

import asyncio
import sys
sys.path.append('..')

from scheduler.engine import SchedulerEngine


async def main():
    """执行公司调研流程"""
    
    # 创建调度引擎
    scheduler = SchedulerEngine()
    
    # 定义要调研的公司列表
    companies = [
        "Notion",
        "Grammarly",
        "Figma",
        "ElevenLabs",
        "Runway"
    ]
    
    # 执行公司调研流程
    print("="*60)
    print("🔬 开始执行每日公司调研流程")
    print("="*60)
    print(f"调研公司: {', '.join(companies)}")
    
    result = await scheduler.execute_company_research(companies)
    
    # 输出结果
    print("\n" + "="*60)
    print("📊 执行结果")
    print("="*60)
    print(f"成功: {result.get('success')}")
    print(f"调研报告数量: {len(result.get('research_reports', []))}")
    print(f"洞察: {result.get('insight', 'N/A')[:100]}...")
    
    # 获取任务摘要
    summary = scheduler.get_task_summary()
    print(f"\n任务摘要: {summary}")


if __name__ == "__main__":
    asyncio.run(main())
