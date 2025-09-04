---
applyTo: '**/*.py'
---

# Prediction Market Arbitrage Bot - Crawl4AI Implementation

## Project Overview
Prediction markets arbitrage system using Crawl4AI v0.7.4. Successfully implemented foundational crawling architecture following official documentation patterns.

## Current Status: ✅ PHASE 1 COMPLETE

### ✅ Working Implementation
- **Foundation**: All basic crawling patterns implemented and tested
- **Multi-Platform**: Concurrent crawling of 5 prediction market platforms
- **Performance**: 71% faster with parallel processing (3.95s vs 6.76s)
- **Success Rate**: 100% (5/5 platforms crawled successfully)

### Implementation Architecture

#### Official Crawl4AI Patterns Used:
1. **AsyncWebCrawler Context Manager** (from `hello_world.py`)
2. **Multi-URL Concurrent Crawling** (from `async_webcrawler_multiple_urls_example.py`)
3. **Structured Data Extraction** (from `extraction_strategies_examples.py`)
4. **Dispatcher Configuration** (from `arun_vs_arun_many.py`)

#### Working Scripts:
```
/arbitrage_bot/
├── main.py                           # Basic test (hello_world.py pattern)
├── single_market_monitor.py          # Single URL (hello_world.py pattern)
├── multi_platform_crawler.py         # Multi-URL (async_webcrawler_multiple_urls_example.py)
├── structured_extraction.py          # JSON CSS extraction (extraction_strategies_examples.py)
├── advanced_concurrent_crawler.py    # Dispatcher optimization (arun_vs_arun_many.py)
└── run_monitors.sh                   # Shell orchestration
```

## NEXT PHASE: Real Market Data Extraction

### Current Gap
- ✅ Successfully crawling all prediction market sites
- ❌ **Missing**: Actual betting odds and market prices
- ❌ **Need**: Real CSS selectors for market data
- ❌ **Need**: Arbitrage detection logic

### Phase 2 Implementation Plan

#### 1. Market Data Extraction Schemas
```python
# Example: Real PredictIt schema (needs actual CSS selectors)
predictit_schema = {
    "name": "PredictItMarkets",
    "baseSelector": "[data-testid='market-card']",  # Real selector needed
    "fields": [
        {"name": "event_title", "selector": ".market-title", "type": "text"},
        {"name": "yes_price", "selector": ".yes-price", "type": "text"},
        {"name": "no_price", "selector": ".no-price", "type": "text"},
        {"name": "volume", "selector": ".volume", "type": "text"}
    ]
}
```

#### 2. Multi-Platform Configuration
```python
# Following official multi-URL pattern
configs = [
    CrawlerRunConfig(
        url_matcher=["*predictit.org*"],
        extraction_strategy=JsonCssExtractionStrategy(predictit_schema)
    ),
    CrawlerRunConfig(
        url_matcher=["*polymarket.com*"],
        extraction_strategy=JsonCssExtractionStrategy(polymarket_schema)
    )
]
```

#### 3. Arbitrage Detection
```python
def detect_arbitrage(market_data):
    """
    Arbitrage formula: (1/odds_A) + (1/odds_B) < 1
    If true, guaranteed profit exists
    """
    for event in normalized_events:
        total_implied_probability = sum(1/odds for odds in event.all_odds)
        if total_implied_probability < 1.0:
            yield ArbitrageOpportunity(event, profit_margin=1.0-total_implied_probability)
```

## Development Guidelines

### Code Standards
- **Follow Official Patterns**: All implementations must reference official Crawl4AI examples
- **Error Handling**: Use async context managers for proper resource cleanup
- **Performance**: Prefer `arun_many()` over sequential `arun()` calls
- **Documentation**: Reference specific official examples used

### Required Dependencies
```
crawl4ai>=0.7.4
playwright>=1.40.0
asyncio
aiohttp
beautifulsoup4
```

### Testing Protocol
1. Test basic crawling with `main.py`
2. Validate single platform with `single_market_monitor.py`
3. Test multi-platform with `multi_platform_crawler.py`
4. Verify concurrent performance with `advanced_concurrent_crawler.py`

## Platform-Specific Implementation Notes

### Supported Platforms:
- **PredictIt**: Markets page crawling ✅
- **Polymarket**: Homepage crawling ✅  
- **Kalshi**: Markets page crawling ✅
- **Manifold**: Homepage crawling ✅
- **Betfair**: Politics section crawling ✅

### CSS Selector Research Needed:
- Inspect actual HTML structure of each platform
- Identify market containers, event titles, odds/prices
- Test extraction schemas with real data
- Handle dynamic content loading

## Next Action Items

1. **Research Real CSS Selectors**: Inspect HTML of prediction market pages
2. **Implement Market Data Schemas**: Create extraction strategies for actual betting data
3. **Build Arbitrage Logic**: Implement price comparison and opportunity detection
4. **Add Data Persistence**: Store market data for historical analysis
5. **Create Monitoring**: Add scheduling and notification systems

## Performance Benchmarks
- **Sequential Crawling**: 6.76 seconds
- **Parallel (with rate limit)**: 4.09 seconds
- **Parallel (no rate limit)**: 3.95 seconds
- **Success Rate**: 100% across all platforms

## Official Documentation References
- Base Implementation: `/workspaces/crawl4ai/docs/examples/`
- Multi-URL Crawling: `async_webcrawler_multiple_urls_example.py`
- Extraction Strategies: `extraction_strategies_examples.py`
- Performance Optimization: `arun_vs_arun_many.py`