"""
Multi-Platform Prediction Market Crawler
Based on official Crawl4AI async_webcrawler_multiple_urls_example.py
Reference: /workspaces/crawl4ai/docs/examples/async_webcrawler_multiple_urls_example.py

This script follows the exact pattern from the official multiple URLs example,
only changing the URLs to monitor different prediction market platforms.
"""
import asyncio
from crawl4ai import AsyncWebCrawler


async def main():
    """
    Official pattern from async_webcrawler_multiple_urls_example.py:
    1. Initialize AsyncWebCrawler with verbose=True
    2. Define list of URLs to crawl
    3. Set up crawling parameters
    4. Use arun_many() for concurrent crawling
    5. Process results in a loop
    """
    # Initialize the AsyncWebCrawler - exact pattern from official example
    async with AsyncWebCrawler(verbose=True) as crawler:
        # List of prediction market URLs - only URLs changed from official example
        urls = [
            "https://www.predictit.org/markets",
            "https://polymarket.com/",
            "https://kalshi.com/markets",
            "https://manifold.markets/",
            "https://www.betfair.com/exchange/plus/politics"
        ]

        # Set up crawling parameters - same as official example
        word_count_threshold = 100

        # Run the crawling process for multiple URLs - exact pattern from official
        results = await crawler.arun_many(
            urls=urls,
            word_count_threshold=word_count_threshold,
            bypass_cache=True,
            verbose=True,
        )

        # Process the results - exact pattern from official example
        print("=== Multi-Platform Prediction Market Results ===")
        for result in results:
            if result.success:
                print(f"Successfully crawled: {result.url}")
                print(f"Title: {result.metadata.get('title', 'N/A')}")
                print(f"Word count: {len(result.markdown.split())}")
                print(
                    f"Number of links: {len(result.links.get('internal', [])) + len(result.links.get('external', []))}"
                )
                print(f"Number of images: {len(result.media.get('images', []))}")
                print("---")
            else:
                print(f"Failed to crawl: {result.url}")
                print(f"Error: {result.error_message}")
                print("---")


if __name__ == "__main__":
    asyncio.run(main())