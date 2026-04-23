"""
内容生产流程示例
展示如何使用调度引擎执行内容生产任务
"""

import asyncio
import sys
sys.path.append('..')

from scheduler.engine import SchedulerEngine


async def main():
    """执行内容生产流程"""
    
    # 创建调度引擎
    scheduler = SchedulerEngine()
    
    # 执行内容生产流程
    print("="*60)
    print("🌅 开始执行每日内容生产流程")
    print("="*60)
    
    result = await scheduler.execute_content_production()
    
    # 输出结果
    print("\n" + "="*60)
    print("📊 执行结果")
    print("="*60)
    print(f"成功: {result.get('success')}")
    print(f"热点选题: {result.get('hot_scout', 'N/A')[:100]}...")
    print(f"内容: {result.get('content', 'N/A')[:100]}...")
    print(f"配图: {'已生成' if result.get('images') else 'N/A'}")
    print(f"质检: {'通过' if result.get('qa_passed') else '不通过'}")
    
    # 获取任务摘要
    summary = scheduler.get_task_summary()
    print(f"\n任务摘要: {summary}")


if __name__ == "__main__":
    asyncio.run(main())
