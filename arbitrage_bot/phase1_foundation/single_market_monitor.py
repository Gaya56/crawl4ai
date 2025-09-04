"""
Prediction Market Monitor - Single URL Pattern
Based on official Crawl4AI hello_world.py example
Reference: /workspaces/crawl4ai/docs/examples/hello_world.py

This script follows the exact pattern from the official hello_world.py example,
only changing the URL to monitor prediction markets.
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
    Official pattern from hello_world.py:
    1. Create BrowserConfig
    2. Use AsyncWebCrawler in async context manager
    3. Create CrawlerRunConfig
    4. Call arun() for single URL
    5. Process CrawlResult
    """
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
        # Only URL changed from official example - using PredictIt market page
        result: CrawlResult = await crawler.arun(
            url="https://www.predictit.org/markets", config=crawler_config
        )
        print("=== PredictIt Markets Data ===")
        print(f"URL: {result.url}")
        print(f"Success: {result.success}")
        print(f"Title: {result.metadata.get('title', 'N/A')}")
        print(f"Markdown Length: {len(result.markdown.raw_markdown)}")
        print("First 500 chars of markdown:")
        print(result.markdown.raw_markdown[:500])

if __name__ == "__main__":
    asyncio.run(main())