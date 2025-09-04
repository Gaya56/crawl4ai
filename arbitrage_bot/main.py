import asyncio
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig
from crawl4ai import JsonCssExtractionStrategy

# --- Configuration Section ---
# For testing, we'll use a simple website with predictable structure
URL_TO_CRAWL = "https://news.ycombinator.com/"

# Test schema for Hacker News (we know this structure)
TEST_SCHEMA = {
    "name": "HackerNewsStories",
    "baseSelector": "tr.athing",  # Each story row
    "fields": [
        {
            "name": "title",
            "selector": "span.titleline a",
            "type": "text"
        },
        {
            "name": "link",
            "selector": "span.titleline a",
            "type": "attribute",
            "attribute": "href"
        },
        {
            "name": "story_id",
            "selector": "",
            "type": "attribute", 
            "attribute": "id"
        }
    ]
}

# Future prediction market schema template (to be customized later)
PREDICTION_MARKET_SCHEMA = {
    "name": "MarketOdds",
    "baseSelector": ".event-market-container",  # A container for a single event/market
    "fields": [
        {
            "name": "event_title",
            "selector": "h2.event-title",
            "type": "text"
        },
        {
            "name": "outcome_name",
            "selector": ".outcome-name",
            "type": "text"
        },
        {
            "name": "price_odds",
            "selector": ".outcome-price",
            "type": "text"
        }
    ]
}

async def main():
    """
    Main function to run the arbitrage bot.
    This script performs a single crawl on a prediction market website
    and extracts structured data based on a predefined schema.
    """
    print("=== Phase 1: Testing Single-Source Data Extraction ===")
    print("Using Hacker News as a test site to validate our extraction approach...")

    # 1. Define the extraction strategy using the test schema
    extraction_strategy = JsonCssExtractionStrategy(schema=TEST_SCHEMA)

    # 2. Configure the crawler run
    config = CrawlerRunConfig(extraction_strategy=extraction_strategy)

    # 3. Initialize and run the crawler
    async with AsyncWebCrawler() as crawler:
        print(f"Crawling URL: {URL_TO_CRAWL}")
        result = await crawler.arun(url=URL_TO_CRAWL, config=config)

        # 4. Process and display the result
        print(f"\nURL: {result.url}")
        print(f"Success: {result.success}")
        
        if result.success:
            if result.extracted_content:
                try:
                    # The result from JsonCssExtractionStrategy is a JSON string
                    extracted_data = json.loads(result.extracted_content)
                    print("✅ Extraction successful!")
                    print(f"Extracted {len(extracted_data)} items:")
                    
                    # Show first few items
                    for j, item in enumerate(extracted_data[:3]):
                        print(f"  {j + 1}. {item}")
                        
                    if len(extracted_data) > 3:
                        print(f"  ... and {len(extracted_data) - 3} more items")
                        
                except json.JSONDecodeError as e:
                    print(f"❌ JSON parsing error: {e}")
                    print(f"Raw extracted content: {result.extracted_content[:200]}...")
            else:
                print("⚠️  Extraction did not yield any data. This could be because:")
                print("   - The CSS selectors in the schema are incorrect for the target site.")
                print("   - The 'baseSelector' did not find any matching elements on the page.")
        else:
            print(f"❌ Crawl failed for URL: {result.url}")
            if hasattr(result, 'error') and result.error:
                print(f"   Error: {result.error}")

    print("\n=== Phase 1 Complete ===")
    print("✅ If you see extracted data above, our approach is working!")
    print("Next: We'll adapt this to real prediction market sites...")

if __name__ == "__main__":
    asyncio.run(main())
