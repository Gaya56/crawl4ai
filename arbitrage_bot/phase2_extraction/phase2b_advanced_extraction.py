"""
Phase 2B: Advanced Market Data Extraction with JavaScript
Targeting specific markets and handling dynamic content
"""
import asyncio
import json
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai import JsonCssExtractionStrategy
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator


async def extract_dynamic_market_data():
    """
    Extract market data with JavaScript execution for dynamic content
    """
    browser_config = BrowserConfig(headless=True, verbose=True)
    
    # More specific market URLs and JS to handle dynamic loading
    market_configs = [
        {
            "url": "https://www.predictit.org/markets/21/Elections",
            "name": "PredictIt_Elections",
            "js_code": [
                # Wait for market cards to load
                "await new Promise(resolve => setTimeout(resolve, 3000));",
                # Click to show more markets if button exists
                "const showMore = document.querySelector('button[contains(text(), \"Show\")]'); if(showMore) showMore.click();"
            ],
            "wait_for": "div[class*='market'], .market-card, article",
            "schema": {
                "name": "PredictItElections",
                "baseSelector": "div[class*='market'], article, .card",
                "fields": [
                    {"name": "title", "selector": "h1, h2, h3, .title, [data-test*='title']", "type": "text"},
                    {"name": "yes_price", "selector": ".yes, [class*='yes'], .buy-yes", "type": "text"},
                    {"name": "no_price", "selector": ".no, [class*='no'], .buy-no", "type": "text"},
                    {"name": "all_prices", "selector": "[class*='price'], .price", "type": "text"},
                    {"name": "links", "selector": "a", "type": "attribute", "attribute": "href"}
                ]
            }
        },
        {
            "url": "https://polymarket.com/event/presidential-election-winner-2024",
            "name": "Polymarket_Election", 
            "js_code": [
                # Wait for React app to load
                "await new Promise(resolve => setTimeout(resolve, 5000));",
                # Scroll to trigger lazy loading
                "window.scrollTo(0, document.body.scrollHeight);",
                "await new Promise(resolve => setTimeout(resolve, 2000));"
            ],
            "wait_for": "[data-testid], .market, .outcome",
            "schema": {
                "name": "PolymarketElection",
                "baseSelector": "div[class*='outcome'], div[class*='market'], [data-testid]",
                "fields": [
                    {"name": "outcome_text", "selector": "*", "type": "text"},
                    {"name": "price", "selector": "[class*='price'], .price, .cost", "type": "text"},
                    {"name": "percentage", "selector": "[class*='percent'], .percent", "type": "text"}
                ]
            }
        }
    ]
    
    async with AsyncWebCrawler(config=browser_config) as crawler:
        for market_config in market_configs:
            print(f"\n=== Extracting {market_config['name']} ===")
            
            extraction_strategy = JsonCssExtractionStrategy(market_config['schema'])
            
            config = CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                extraction_strategy=extraction_strategy,
                js_code=market_config.get('js_code', []),
                wait_for=market_config.get('wait_for'),
                markdown_generator=DefaultMarkdownGenerator(
                    content_filter=PruningContentFilter()
                ),
            )
            
            result = await crawler.arun(url=market_config['url'], config=config)
            
            if result.success:
                print(f"✅ Successfully crawled: {result.url}")
                print(f"Title: {result.metadata.get('title', 'N/A')}")
                
                try:
                    extracted_data = json.loads(result.extracted_content)
                    print(f"📊 Extracted {len(extracted_data)} items")
                    
                    # Look for actual market data
                    market_items = []
                    for item in extracted_data:
                        # Filter items that contain price-like data
                        has_price_data = any(
                            key in str(item).lower() for key in ['price', 'yes', 'no', '%', '$', '¢']
                        )
                        if has_price_data:
                            market_items.append(item)
                    
                    print(f"💰 Found {len(market_items)} items with potential market data")
                    
                    # Show first few market items
                    for i, item in enumerate(market_items[:5]):
                        print(f"\nMarket Item {i+1}:")
                        for key, value in item.items():
                            if value and len(str(value)) < 200:
                                print(f"  {key}: {value}")
                                
                except json.JSONDecodeError:
                    print("❌ Could not parse extracted JSON")
                    print(f"Raw content preview: {result.extracted_content[:300]}...")
                
                # Show markdown sample for context
                print(f"\n📄 Markdown sample (first 400 chars):")
                print(result.markdown.raw_markdown[:400])
                
            else:
                print(f"❌ Failed to crawl {market_config['name']}: {result.error_message}")


async def main():
    print("=== Phase 2B: Advanced Market Data Extraction ===")
    print("Targeting specific markets with JavaScript execution...")
    await extract_dynamic_market_data()


if __name__ == "__main__":
    asyncio.run(main())