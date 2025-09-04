import asyncio
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai import JsonCssExtractionStrategy

# --- Phase 2: Multi-Platform Configuration ---

# Different schemas for different prediction market sites
# These are templates - you'll need to inspect actual sites to get correct selectors

PREDICTIT_SCHEMA = {
    "name": "PredictItMarkets",
    "baseSelector": ".market-card",  # Example selector
    "fields": [
        {
            "name": "event_title",
            "selector": ".market-title",
            "type": "text"
        },
        {
            "name": "outcome_name", 
            "selector": ".outcome-name",
            "type": "text"
        },
        {
            "name": "yes_price",
            "selector": ".yes-price",
            "type": "text"
        },
        {
            "name": "no_price",
            "selector": ".no-price", 
            "type": "text"
        }
    ]
}

POLYMARKET_SCHEMA = {
    "name": "PolymarketEvents",
    "baseSelector": ".event-container",  # Example selector
    "fields": [
        {
            "name": "event_title",
            "selector": "h3.event-name",
            "type": "text"
        },
        {
            "name": "outcome_name",
            "selector": ".outcome-title",
            "type": "text"
        },
        {
            "name": "price_odds",
            "selector": ".price-display",
            "type": "text"
        }
    ]
}

KALSHI_SCHEMA = {
    "name": "KalshiMarkets", 
    "baseSelector": ".market-row",  # Example selector
    "fields": [
        {
            "name": "event_title",
            "selector": ".market-question",
            "type": "text"
        },
        {
            "name": "outcome_name",
            "selector": ".outcome-label",
            "type": "text"
        },
        {
            "name": "price_cents",
            "selector": ".price-value",
            "type": "text"
        }
    ]
}

# For testing purposes, we'll use sites we know work
TEST_URLS_AND_CONFIGS = [
    {
        "url": "https://news.ycombinator.com/",
        "name": "HackerNews",
        "schema": {
            "name": "HackerNewsStories",
            "baseSelector": "tr.athing",
            "fields": [
                {"name": "title", "selector": "span.titleline a", "type": "text"},
                {"name": "link", "selector": "span.titleline a", "type": "attribute", "attribute": "href"}
            ]
        }
    },
    {
        "url": "https://example.com/",
        "name": "Example",
        "schema": {
            "name": "ExampleContent",
            "baseSelector": "body",
            "fields": [
                {"name": "title", "selector": "h1", "type": "text"},
                {"name": "content", "selector": "p", "type": "text"}
            ]
        }
    },
    {
        "url": "https://httpbin.org/html",
        "name": "HTTPBin",
        "schema": {
            "name": "HTMLContent",
            "baseSelector": "body",
            "fields": [
                {"name": "title", "selector": "h1", "type": "text"},
                {"name": "description", "selector": "p", "type": "text"}
            ]
        }
    }
]

# Future real prediction market URLs (to be used once we have the correct schemas)
PREDICTION_MARKET_URLS = [
    {
        "url": "https://www.predictit.org/markets",
        "name": "PredictIt", 
        "schema": PREDICTIT_SCHEMA
    },
    {
        "url": "https://polymarket.com/",
        "name": "Polymarket",
        "schema": POLYMARKET_SCHEMA  
    },
    {
        "url": "https://kalshi.com/markets",
        "name": "Kalshi",
        "schema": KALSHI_SCHEMA
    }
]

async def test_multi_platform_crawling():
    """
    Phase 2: Test multi-platform crawling with different configurations
    """
    print("=== Phase 2: Multi-Platform Price Aggregation ===")
    print("Testing concurrent crawling of multiple sources...")

    # Create configurations for each URL
    configs = []
    urls = []
    
    for site_config in TEST_URLS_AND_CONFIGS:
        # Create extraction strategy for this site
        extraction_strategy = JsonCssExtractionStrategy(schema=site_config["schema"])
        
        # Create crawler config with URL matcher
        config = CrawlerRunConfig(
            url_matcher=[f"*{site_config['url'].split('//')[1].split('/')[0]}*"],
            extraction_strategy=extraction_strategy
        )
        
        configs.append(config)
        urls.append(site_config["url"])
        print(f"  📊 Configured: {site_config['name']} - {site_config['url']}")

    print(f"\n🚀 Starting concurrent crawl of {len(urls)} URLs...")
    
    # Initialize crawler and run multiple URLs concurrently
    async with AsyncWebCrawler() as crawler:
        # Use arun_many for concurrent execution
        results = await crawler.arun_many(urls=urls, config=configs)
        
        print(f"\n📊 Crawl Results Summary:")
        print("="*50)
        
        for i, result in enumerate(results):
            site_name = TEST_URLS_AND_CONFIGS[i]["name"]
            print(f"\n{i+1}. {site_name} ({result.url})")
            print(f"   Status: {'✅ Success' if result.success else '❌ Failed'}")
            
            if result.success and result.extracted_content:
                try:
                    extracted_data = json.loads(result.extracted_content)
                    print(f"   Data: {len(extracted_data)} items extracted")
                    
                    # Show sample data
                    if extracted_data:
                        sample = extracted_data[0] if isinstance(extracted_data, list) else extracted_data
                        print(f"   Sample: {str(sample)[:100]}...")
                        
                except json.JSONDecodeError as e:
                    print(f"   Error: JSON parsing failed - {e}")
            elif result.success:
                print(f"   Warning: No data extracted (check selectors)")
            else:
                print(f"   Error: Crawl failed")

    print("\n=== Phase 2 Complete ===")
    print("✅ Multi-platform crawling tested!")
    print("Next: We'll add arbitrage detection logic and data persistence...")

async def main():
    await test_multi_platform_crawling()

if __name__ == "__main__":
    asyncio.run(main())