"""
Phase 2: Real Market Data Extraction
Based on official Crawl4AI structured extraction patterns

This script demonstrates how to extract actual betting odds and market data
from prediction market platforms using proper CSS selectors.
"""
import asyncio
import json
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai import JsonCssExtractionStrategy
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator


def create_market_schemas():
    """
    Create extraction schemas for different prediction market platforms.
    These are educated guesses based on common HTML patterns - will need refinement.
    """
    
    # PredictIt schema (needs real CSS selectors from HTML inspection)
    predictit_schema = {
        "name": "PredictItMarkets",
        "baseSelector": "div[class*='market'], article[class*='market'], .market-container",
        "fields": [
            {"name": "event_title", "selector": "h1, h2, h3, .title, [class*='title']", "type": "text"},
            {"name": "market_name", "selector": ".market-name, [class*='market-name'], [data-test*='market']", "type": "text"},
            {"name": "yes_price", "selector": ".yes, [class*='yes'], [data-test*='yes']", "type": "text"},
            {"name": "no_price", "selector": ".no, [class*='no'], [data-test*='no']", "type": "text"},
            {"name": "price", "selector": ".price, [class*='price'], .odds", "type": "text"},
            {"name": "volume", "selector": ".volume, [class*='volume']", "type": "text"}
        ]
    }
    
    # Polymarket schema (broader selectors to catch market data)
    polymarket_schema = {
        "name": "PolymarketData",
        "baseSelector": "div[class*='market'], div[class*='card'], article",
        "fields": [
            {"name": "question", "selector": "h1, h2, h3, .question, [class*='question']", "type": "text"},
            {"name": "outcome", "selector": ".outcome, [class*='outcome']", "type": "text"},
            {"name": "probability", "selector": ".probability, [class*='prob'], .percentage", "type": "text"},
            {"name": "price", "selector": ".price, [class*='price'], .cost", "type": "text"},
            {"name": "volume", "selector": ".volume, [class*='volume'], .liquidity", "type": "text"}
        ]
    }
    
    # Kalshi schema
    kalshi_schema = {
        "name": "KalshiMarkets",
        "baseSelector": "div[class*='market'], div[class*='event'], .market-item",
        "fields": [
            {"name": "event_title", "selector": "h1, h2, h3, .title, [class*='title']", "type": "text"},
            {"name": "yes_price", "selector": ".yes, [class*='yes'], .buy", "type": "text"},
            {"name": "no_price", "selector": ".no, [class*='no'], .sell", "type": "text"},
            {"name": "volume", "selector": ".volume, [class*='volume']", "type": "text"}
        ]
    }
    
    return {
        "predictit": predictit_schema,
        "polymarket": polymarket_schema, 
        "kalshi": kalshi_schema
    }


async def inspect_page_structure(url, platform_name):
    """
    First, let's see what we can extract with broad selectors to understand the structure
    """
    browser_config = BrowserConfig(headless=True, verbose=True)
    
    # Generic inspection schema
    inspection_schema = {
        "name": f"{platform_name}Inspection",
        "baseSelector": "div",  # Very broad selector
        "fields": [
            {"name": "all_text", "selector": "*", "type": "text"},
            {"name": "links", "selector": "a", "type": "attribute", "attribute": "href"},
            {"name": "prices", "selector": "[class*='price'], [class*='odds'], [class*='cost']", "type": "text"},
            {"name": "buttons", "selector": "button", "type": "text"}
        ]
    }
    
    extraction_strategy = JsonCssExtractionStrategy(inspection_schema)
    
    async with AsyncWebCrawler(config=browser_config) as crawler:
        config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            extraction_strategy=extraction_strategy,
            markdown_generator=DefaultMarkdownGenerator(
                content_filter=PruningContentFilter()
            ),
        )
        
        result = await crawler.arun(url=url, config=config)
        
        if result.success:
            print(f"\n=== {platform_name} Structure Analysis ===")
            print(f"URL: {result.url}")
            print(f"Page Title: {result.metadata.get('title', 'N/A')}")
            print(f"Markdown Length: {len(result.markdown.raw_markdown)} chars")
            
            # Try to parse extracted content
            try:
                extracted_data = json.loads(result.extracted_content)
                print(f"Extracted Items: {len(extracted_data)}")
                
                # Show first few items to understand structure
                for i, item in enumerate(extracted_data[:3]):
                    print(f"\nItem {i+1}:")
                    for key, value in item.items():
                        if value and len(str(value)) < 100:  # Only show non-empty, short values
                            print(f"  {key}: {value}")
                            
            except json.JSONDecodeError:
                print("Could not parse extracted content as JSON")
                print(f"Raw content preview: {result.extracted_content[:200]}...")
                
            # Also show some raw markdown to understand page structure
            print(f"\nFirst 500 chars of markdown:")
            print(result.markdown.raw_markdown[:500])
            
        else:
            print(f"Failed to crawl {platform_name}: {result.error_message}")


async def extract_market_data():
    """
    Main function to extract actual market data from prediction platforms
    """
    print("=== Phase 2: Real Market Data Extraction ===")
    print("Analyzing page structures and attempting data extraction...")
    
    # Test URLs - using specific market pages where possible
    test_urls = [
        ("https://www.predictit.org/markets", "PredictIt"),
        ("https://polymarket.com/", "Polymarket"),
        ("https://kalshi.com/markets", "Kalshi")
    ]
    
    for url, platform_name in test_urls:
        await inspect_page_structure(url, platform_name)
        print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(extract_market_data())