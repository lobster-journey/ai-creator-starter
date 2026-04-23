#!/usr/bin/env python3
"""
🦞 龙虾巡游记 - 小红书发布测试
直接使用Playwright + Cookie实现发布功能
"""

import json
import asyncio
import logging
from pathlib import Path
from typing import List, Optional

# 尝试导入playwright
try:
    from playwright.async_api import async_playwright, Browser, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️ Playwright未安装，请运行: pip install playwright && playwright install chromium")

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('LobsterJourney.PublishTest')


class XiaohongshuPublisher:
    """小红书发布器"""
    
    def __init__(self, cookies_path: str = "/tmp/xhs-cookies/cookies.json"):
        self.cookies_path = cookies_path
        self.cookies = self._load_cookies()
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        
    def _load_cookies(self) -> List[dict]:
        """加载Cookie"""
        try:
            with open(self.cookies_path, 'r') as f:
                cookies = json.load(f)
                logger.info(f"✅ 加载Cookie成功，共 {len(cookies)} 个")
                return cookies
        except FileNotFoundError:
            logger.error(f"❌ Cookie文件不存在: {self.cookies_path}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"❌ Cookie格式错误: {e}")
            return []
    
    async def init_browser(self):
        """初始化浏览器"""
        if not PLAYWRIGHT_AVAILABLE:
            raise RuntimeError("Playwright未安装")
        
        logger.info("🚀 启动浏览器...")
        playwright = await async_playwright().start()
        
        # 启动浏览器
        self.browser = await playwright.chromium.launch(
            headless=True,  # 无头模式
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
            ]
        )
        
        # 创建上下文
        context = await self.browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        # 添加Cookie
        if self.cookies:
            await context.add_cookies(self.cookies)
            logger.info("✅ Cookie已注入")
        
        # 创建页面
        self.page = await context.new_page()
        
        # 注入反检测脚本
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        logger.info("✅ 浏览器初始化完成")
    
    async def check_login(self) -> bool:
        """检查登录状态"""
        if not self.page:
            await self.init_browser()
        
        logger.info("🔍 检查登录状态...")
        
        try:
            # 访问小红书首页
            await self.page.goto('https://www.xiaohongshu.com', wait_until='networkidle', timeout=30000)
            await asyncio.sleep(2)
            
            # 截图保存
            screenshot_path = "/tmp/xhs-cookies/homepage.png"
            await self.page.screenshot(path=screenshot_path)
            logger.info(f"📸 首页截图已保存: {screenshot_path}")
            
            # 检查登录状态
            # 尝试查找用户相关元素
            user_menu = await self.page.locator('.user-info, .login-btn, [class*="user"]').count()
            
            if user_menu > 0:
                logger.info(f"✅ 检测到用户元素: {user_menu} 个")
                return True
            else:
                logger.warning("⚠️ 未检测到用户元素，可能未登录")
                return False
                
        except Exception as e:
            logger.error(f"❌ 检查登录失败: {e}")
            return False
    
    async def publish_note(
        self,
        title: str,
        content: str,
        images: List[str] = None,
        tags: List[str] = None
    ) -> dict:
        """
        发布笔记
        
        Args:
            title: 标题
            content: 内容
            images: 图片路径列表
            tags: 标签列表
        
        Returns:
            发布结果
        """
        if not self.page:
            await self.init_browser()
        
        logger.info(f"📝 准备发布笔记: {title}")
        
        try:
            # 访问创作者中心
            logger.info("🌐 访问创作者中心...")
            await self.page.goto(
                'https://creator.xiaohongshu.com/publish/publish',
                wait_until='networkidle',
                timeout=30000
            )
            await asyncio.sleep(2)
            
            # 截图
            screenshot_path = "/tmp/xhs-cookies/creator-center.png"
            await self.page.screenshot(path=screenshot_path)
            logger.info(f"📸 创作者中心截图: {screenshot_path}")
            
            # 检查是否需要登录
            current_url = self.page.url
            if 'login' in current_url:
                logger.error("❌ 需要重新登录")
                return {
                    "success": False,
                    "message": "需要重新登录"
                }
            
            # TODO: 实现完整的发布流程
            # 1. 上传图片
            # 2. 填写标题
            # 3. 填写内容
            # 4. 添加标签
            # 5. 点击发布
            
            logger.info("⚠️ 发布流程待完整实现")
            
            return {
                "success": True,
                "message": "已到达发布页面，待实现完整流程",
                "url": current_url
            }
            
        except Exception as e:
            logger.error(f"❌ 发布失败: {e}")
            return {
                "success": False,
                "message": str(e)
            }
    
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
            logger.info("🔒 浏览器已关闭")


async def test_publish():
    """测试发布"""
    print("🦞 龙虾巡游记 - 发布测试")
    print("=" * 50)
    
    # 创建发布器
    publisher = XiaohongshuPublisher()
    
    try:
        # 初始化浏览器
        await publisher.init_browser()
        
        # 检查登录状态
        logged_in = await publisher.check_login()
        
        if not logged_in:
            print("❌ 登录状态无效，请更新Cookie")
            return
        
        # 测试发布
        print("\n📝 测试发布...")
        result = await publisher.publish_note(
            title="🦞 龙虾巡游记 - 测试笔记",
            content="这是一条测试内容\n\n#龙虾巡游记 #AI博主",
            images=["/tmp/test.jpg"],
            tags=["龙虾巡游记", "AI博主"]
        )
        
        print(f"\n发布结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await publisher.close()
    
    print("\n" + "=" * 50)
    print("测试完成！")


def main():
    """主函数"""
    if not PLAYWRIGHT_AVAILABLE:
        print("❌ Playwright未安装")
        print("\n请运行以下命令安装:")
        print("  pip install playwright")
        print("  playwright install chromium")
        return
    
    asyncio.run(test_publish())


if __name__ == "__main__":
    main()
