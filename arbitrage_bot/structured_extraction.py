"""
Structured Prediction Market Data Extraction
Based on official Crawl4AI extraction_strategies_examples.py
Reference: /workspaces/crawl4ai/docs/examples/extraction_strategies_examples.py

This script follows the exact pattern from the official extraction strategies example,
using JsonCssExtractionStrategy for structured data extraction from prediction markets.
"""
import asyncio
import os

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai import (
    JsonCssExtractionStrategy,
)
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator


async def run_extraction(crawler: AsyncWebCrawler, url: str, strategy, name: str):
    """
    Helper function from official example - exact same implementation
    Reference: extraction_strategies_examples.py run_extraction()
    """
    try:
        # Configure the crawler run settings - exact pattern from official
        config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            extraction_strategy=strategy,
            markdown_generator=DefaultMarkdownGenerator(
                content_filter=PruningContentFilter()  # For fit_markdown support
            ),
        )

        # Run the crawler - exact pattern from official
        result = await crawler.arun(url=url, config=config)

        if result.success:
            print(f"\n=== {name} Results ===")
            print(f"URL: {result.url}")
            print(f"Extracted Content: {result.extracted_content}")
            print(f"Raw Markdown Length: {len(result.markdown.raw_markdown)}")
            print(
                f"Citations Markdown Length: {len(result.markdown.markdown_with_citations)}"
            )
        else:
            print(f"Error in {name}: Crawl failed")

    except Exception as e:
        print(f"Error in {name}: {str(e)}")


async def main():
    """
    Official pattern from extraction_strategies_examples.py:
    1. Define URLs for prediction markets
    2. Configure browser settings
    3. Initialize extraction strategies with JsonCssExtractionStrategy
    4. Use context manager for proper resource handling
    5. Run all strategies
    """
    # Prediction market URLs - only URLs changed from official example
    predictit_url = "https://www.predictit.org/markets"
    polymarket_url = "https://polymarket.com/"

    # Configure browser settings - exact pattern from official
    browser_config = BrowserConfig(headless=True, verbose=True)

    # Initialize extraction strategies following official patterns

    # 1. PredictIt Market Extraction (JSON CSS - automatically uses HTML input)
    predictit_schema = {
        "baseSelector": ".market-item",  # Generic selectors for demonstration
        "fields": [
            {"name": "title", "selector": ".market-title", "type": "text"},
            {"name": "price", "selector": ".market-price", "type": "text"},
            {"name": "volume", "selector": ".market-volume", "type": "text"},
        ],
    }
    predictit_strategy = JsonCssExtractionStrategy(schema=predictit_schema)

    # 2. Polymarket Extraction (JSON CSS - automatically uses HTML input)
    polymarket_schema = {
        "baseSelector": ".market-card",  # Generic selectors for demonstration
        "fields": [
            {"name": "question", "selector": ".question-text", "type": "text"},
            {"name": "odds", "selector": ".odds-display", "type": "text"},
            {"name": "liquidity", "selector": ".liquidity-info", "type": "text"},
        ],
    }
    polymarket_strategy = JsonCssExtractionStrategy(schema=polymarket_schema)

    # Use context manager for proper resource handling - exact pattern from official
    async with AsyncWebCrawler(config=browser_config) as crawler:
        # Run all strategies - exact pattern from official
        await run_extraction(crawler, predictit_url, predictit_strategy, "PredictIt Markets")
        await run_extraction(crawler, polymarket_url, polymarket_strategy, "Polymarket")


if __name__ == "__main__":
    asyncio.run(main())