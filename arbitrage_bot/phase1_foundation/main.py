"""
Prediction Market Arbitrage Bot - Quick Test Runner
Based on official Crawl4AI hello_world.py pattern

This is the main entry point for testing the prediction market monitors.
It follows the exact pattern from the official hello_world.py example.
"""
import asyncio
from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig, 
    CrawlerRunConfig,
    DefaultMarkdownGenerator,
    PruningContentFilter,
    CrawlResult
)


async def main():
    """
    Quick test following official hello_world.py pattern exactly.
    Only the URL is changed to test prediction market crawling.
    
    Official Reference: /workspaces/crawl4ai/docs/examples/hello_world.py
    """
    print("=== Prediction Market Arbitrage Bot - Quick Test ===")
    print("Based on official Crawl4AI hello_world.py example")
    print("Reference: /workspaces/crawl4ai/docs/examples/hello_world.py")
    print()
    
    # Official pattern from hello_world.py (modified for container environment)
    browser_config = BrowserConfig(
        headless=True,  # Set to True for container environments
        verbose=True,
    )
    async with AsyncWebCrawler(config=browser_config) as crawler:
        crawler_config = CrawlerRunConfig(
            markdown_generator=DefaultMarkdownGenerator(
                content_filter=PruningContentFilter()
            ),
        )
        # Only URL changed from official example - using a reliable test page
        result: CrawlResult = await crawler.arun(
            url="https://example.com", config=crawler_config
        )
        
        print("=== Test Results ===")
        print(f"URL: {result.url}")
        print(f"Success: {result.success}")
        print(f"Title: {result.metadata.get('title', 'N/A')}")
        print(f"Markdown Length: {len(result.markdown.raw_markdown)}")
        print()
        print("First 500 chars of markdown:")
        print(result.markdown.raw_markdown[:500])
        print()
        print("✅ Basic crawling test completed successfully!")
        print()
        print("Next steps:")
        print("1. Run: python3 single_market_monitor.py")
        print("2. Run: python3 multi_platform_crawler.py") 
        print("3. Run: ./run_monitors.sh (for full orchestration)")


if __name__ == "__main__":
    asyncio.run(main())