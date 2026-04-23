#!/usr/bin/env python3
"""
龙虾巡游记公司 - 调度引擎
总经理使用此引擎调度各员工（Agent）执行任务
"""

import asyncio
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class TaskType(Enum):
    """任务类型"""
    CONTENT_PRODUCTION = "content_production"  # 内容生产
    COMPANY_RESEARCH = "company_research"       # 公司调研
    DAILY_REVIEW = "daily_review"               # 每日复盘
    HOT_SPOT_SCAN = "hot_spot_scan"             # 热点扫描
    DATA_REPORT = "data_report"                 # 数据简报
    COMPETITOR_TRACK = "competitor_track"       # 竞品追踪
    CONTENT_ANALYSIS = "content_analysis"       # 内容分析
    INTERACTION_CHECK = "interaction_check"     # 互动检查
    REVIEW_PREP = "review_prep"                 # 复盘准备
    SYSTEM_CHECK = "system_check"               # 系统检查


@dataclass
class AgentTask:
    """Agent任务定义"""
    agent_id: str
    task_name: str
    task_description: str
    timeout_seconds: int
    dependencies: List[str] = None  # 依赖的前置任务ID
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class TaskResult:
    """任务执行结果"""
    agent_id: str
    task_name: str
    success: bool
    result: Any
    error: Optional[str] = None
    duration_seconds: float = 0.0


class SchedulerEngine:
    """调度引擎 - 总经理的核心工具"""
    
    def __init__(self):
        self.task_results: Dict[str, TaskResult] = {}
        self.max_retries = 5  # 质检最多返工5次
        
    async def spawn_agent(self, task: AgentTask) -> TaskResult:
        """
        Spawn一个Agent执行任务
        
        实际实现中，这里会调用sessions_spawn工具
        当前为模拟实现
        """
        print(f"[总经理🦞] 启动员工 {task.agent_id} 执行任务: {task.task_name}")
        
        start_time = datetime.now()
        
        try:
            # 模拟调用sessions_spawn
            # result = await sessions_spawn(
            #     agentId=task.agent_id,
            #     task=task.task_description,
            #     timeoutSeconds=task.timeout_seconds
            # )
            
            # 当前为模拟实现
            await asyncio.sleep(2)  # 模拟执行时间
            result = f"[{task.agent_id}] 任务完成: {task.task_name}"
            
            duration = (datetime.now() - start_time).total_seconds()
            
            return TaskResult(
                agent_id=task.agent_id,
                task_name=task.task_name,
                success=True,
                result=result,
                duration_seconds=duration
            )
            
        except asyncio.TimeoutError:
            duration = (datetime.now() - start_time).total_seconds()
            return TaskResult(
                agent_id=task.agent_id,
                task_name=task.task_name,
                success=False,
                result=None,
                error=f"任务超时（{task.timeout_seconds}秒）",
                duration_seconds=duration
            )
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            return TaskResult(
                agent_id=task.agent_id,
                task_name=task.task_name,
                success=False,
                result=None,
                error=str(e),
                duration_seconds=duration
            )
    
    async def execute_serial(self, tasks: List[AgentTask]) -> List[TaskResult]:
        """
        串行执行任务列表
        每个任务等待前一个完成后再启动
        """
        results = []
        
        for task in tasks:
            # 检查依赖是否完成
            if task.dependencies:
                for dep_id in task.dependencies:
                    if dep_id not in self.task_results:
                        return TaskResult(
                            agent_id=task.agent_id,
                            task_name=task.task_name,
                            success=False,
                            result=None,
                            error=f"依赖任务 {dep_id} 未完成"
                        )
            
            # 执行任务
            result = await self.spawn_agent(task)
            results.append(result)
            self.task_results[task.agent_id] = result
            
            # 如果任务失败，记录但继续执行
            if not result.success:
                print(f"[总经理🦞] 警告: 任务 {task.task_name} 失败: {result.error}")
        
        return results
    
    async def execute_parallel(self, tasks: List[AgentTask]) -> List[TaskResult]:
        """
        并发执行任务列表
        所有任务同时启动，等待全部完成
        """
        print(f"[总经理🦞] 并发启动 {len(tasks)} 个员工")
        
        # 创建所有任务
        coroutines = [self.spawn_agent(task) for task in tasks]
        
        # 并发执行
        results = await asyncio.gather(*coroutines, return_exceptions=True)
        
        # 处理结果
        task_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                task_results.append(TaskResult(
                    agent_id=tasks[i].agent_id,
                    task_name=tasks[i].task_name,
                    success=False,
                    result=None,
                    error=str(result)
                ))
            else:
                task_results.append(result)
                self.task_results[tasks[i].agent_id] = result
        
        return task_results
    
    async def execute_with_retry(
        self, 
        task: AgentTask, 
        quality_check_fn=None,
        max_retries: int = 5
    ) -> TaskResult:
        """
        带质量检查和返工的任务执行
        
        Args:
            task: 任务定义
            quality_check_fn: 质量检查函数，返回(bool, str)
            max_retries: 最多返工次数
        
        Returns:
            最终任务结果
        """
        for attempt in range(1, max_retries + 2):  # 初始+5次返工
            print(f"[总经理🦞] 第{attempt}次执行: {task.task_name}")
            
            result = await self.spawn_agent(task)
            
            if not result.success:
                # 执行失败，直接返回
                return result
            
            # 质量检查
            if quality_check_fn:
                passed, feedback = quality_check_fn(result.result)
                
                if passed:
                    print(f"[总经理🦞] ✅ 质检通过: {task.task_name}")
                    return result
                else:
                    print(f"[总经理🦞] ❌ 质检不通过: {feedback}")
                    
                    if attempt <= max_retries:
                        # 返工
                        task.task_description = f"{task.task_description}\n\n【返工反馈】\n{feedback}"
                        continue
                    else:
                        # 超过最大返工次数，选择最优版本
                        print(f"[总经理🦞] ⚠️ 超过最大返工次数({max_retries})，选择当前版本")
                        return result
            else:
                # 无质量检查，直接返回
                return result
        
        return result
    
    async def execute_content_production(self) -> Dict[str, Any]:
        """
        执行每日内容生产流程
        阶段1串行 → 阶段2并发 → 阶段3串行
        """
        print("\n" + "="*60)
        print("🌅 每日内容生产流程启动")
        print("="*60 + "\n")
        
        # 阶段1：热点侦察（串行）
        print("【阶段1】启动热点侦察员...")
        hot_scout_task = AgentTask(
            agent_id="agent-hot-scout",
            task_name="热点快速扫描",
            task_description="搜索今日AI/科技热点Top10，输出选题报告",
            timeout_seconds=1800  # 30分钟
        )
        
        hot_scout_result = await self.spawn_agent(hot_scout_task)
        self.task_results["hot_scout"] = hot_scout_result
        
        if not hot_scout_result.success:
            return {"success": False, "error": "热点侦察失败"}
        
        # 阶段2：文案创作 + 配图（并发）
        print("\n【阶段2】并发启动文案创作员和配图师...")
        
        copywriter_task = AgentTask(
            agent_id="agent-copywriter",
            task_name="文案创作",
            task_description=f"基于选题报告创作小红书笔记：\n{hot_scout_result.result}",
            timeout_seconds=1200  # 20分钟
        )
        
        designer_task = AgentTask(
            agent_id="agent-designer",
            task_name="配图生成",
            task_description="根据选题关键词生成3张配图",
            timeout_seconds=900  # 15分钟
        )
        
        parallel_results = await self.execute_parallel([copywriter_task, designer_task])
        
        copywriter_result = parallel_results[0]
        designer_result = parallel_results[1]
        
        if not copywriter_result.success:
            return {"success": False, "error": "文案创作失败"}
        
        # 阶段3：质检（串行，带返工）
        print("\n【阶段3】启动质检员...")
        
        qa_task = AgentTask(
            agent_id="agent-qa",
            task_name="质量检查",
            task_description=f"检查笔记质量：\n{copywriter_result.result}",
            timeout_seconds=900  # 15分钟
        )
        
        def quality_check(result):
            """质量检查函数"""
            # 这里应该实现实际的质量检查逻辑
            # 当前为模拟实现
            return True, "质检通过"
        
        qa_result = await self.execute_with_retry(
            qa_task, 
            quality_check_fn=quality_check,
            max_retries=self.max_retries
        )
        
        # 汇总结果
        final_result = {
            "success": qa_result.success,
            "hot_scout": hot_scout_result.result,
            "content": copywriter_result.result,
            "images": designer_result.result if designer_result.success else None,
            "qa_passed": qa_result.success
        }
        
        print("\n" + "="*60)
        print("✅ 内容生产流程完成")
        print("="*60 + "\n")
        
        return final_result
    
    async def execute_company_research(self, companies: List[str]) -> Dict[str, Any]:
        """
        执行每日公司调研流程
        阶段1并发（5个调研员）→ 阶段2串行（洞察提炼师）
        """
        print("\n" + "="*60)
        print("🔬 每日公司调研流程启动")
        print("="*60 + "\n")
        
        # 阶段1：5个调研员并发
        print(f"【阶段1】并发启动 {len(companies)} 个调研员...")
        
        researcher_tasks = [
            AgentTask(
                agent_id=f"agent-researcher-{i+1}",
                task_name=f"调研{company}",
                task_description=f"深度调研公司：{company}",
                timeout_seconds=900  # 15分钟
            )
            for i, company in enumerate(companies)
        ]
        
        research_results = await self.execute_parallel(researcher_tasks)
        
        # 检查是否全部成功
        failed_count = sum(1 for r in research_results if not r.success)
        if failed_count > 0:
            print(f"[总经理🦞] 警告: {failed_count} 个调研任务失败")
        
        # 阶段2：洞察提炼师（串行）
        print("\n【阶段2】启动洞察提炼师...")
        
        research_summaries = "\n\n".join([
            f"### {companies[i]}\n{r.result}"
            for i, r in enumerate(research_results)
            if r.success
        ])
        
        insight_task = AgentTask(
            agent_id="agent-insight",
            task_name="洞察提炼",
            task_description=f"基于调研报告提炼洞察：\n{research_summaries}",
            timeout_seconds=900  # 15分钟
        )
        
        insight_result = await self.spawn_agent(insight_task)
        
        # 汇总结果
        final_result = {
            "success": insight_result.success,
            "research_reports": [r.result for r in research_results if r.success],
            "insight": insight_result.result if insight_result.success else None
        }
        
        print("\n" + "="*60)
        print("✅ 公司调研流程完成")
        print("="*60 + "\n")
        
        return final_result
    
    def get_task_summary(self) -> Dict[str, Any]:
        """获取任务执行摘要"""
        success_count = sum(1 for r in self.task_results.values() if r.success)
        total_count = len(self.task_results)
        
        return {
            "total_tasks": total_count,
            "success_count": success_count,
            "failed_count": total_count - success_count,
            "success_rate": f"{success_count/total_count*100:.1f}%" if total_count > 0 else "N/A"
        }


# 使用示例
async def main():
    """调度引擎使用示例"""
    
    # 创建调度引擎
    scheduler = SchedulerEngine()
    
    # 示例1：执行内容生产流程
    # result = await scheduler.execute_content_production()
    # print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 示例2：执行公司调研流程
    # companies = ["Notion", "Grammarly", "Figma", "ElevenLabs", "Runway"]
    # result = await scheduler.execute_company_research(companies)
    # print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 示例3：获取任务摘要
    # summary = scheduler.get_task_summary()
    # print(json.dumps(summary, ensure_ascii=False, indent=2))
    
    print("调度引擎已就绪，等待定时任务触发...")


if __name__ == "__main__":
    asyncio.run(main())
