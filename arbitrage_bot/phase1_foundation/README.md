# Phase 1: Foundation - Basic Crawling Patterns

This directory contains the foundational crawling scripts that implement official Crawl4AI patterns.

## 📁 Scripts Overview

### `main.py` - Quick Test Runner
- **Based on**: Official `hello_world.py` example
- **Purpose**: Basic functionality test using example.com
- **Pattern**: Single URL crawling with AsyncWebCrawler
- **Usage**: `python3 main.py`

### `single_market_monitor.py` - Single URL Monitor  
- **Based on**: Official `hello_world.py` example
- **Purpose**: Monitor a single prediction market URL
- **Pattern**: Basic arun() pattern with BrowserConfig
- **Target**: PredictIt markets page
- **Usage**: `python3 single_market_monitor.py`

### `multi_platform_crawler.py` - Multi-Platform Crawler
- **Based on**: Official `async_webcrawler_multiple_urls_example.py`
- **Purpose**: Crawl multiple prediction market platforms concurrently
- **Pattern**: arun_many() for concurrent crawling
- **Targets**: PredictIt, Polymarket, Kalshi, Manifold, Betfair
- **Usage**: `python3 multi_platform_crawler.py`

### `structured_extraction.py` - CSS Extraction Framework
- **Based on**: Official `extraction_strategies_examples.py`
- **Purpose**: Demonstrate JsonCssExtractionStrategy patterns
- **Pattern**: Structured data extraction with CSS selectors
- **Note**: Uses placeholder selectors (needs real site inspection)
- **Usage**: `python3 structured_extraction.py`

### `advanced_concurrent_crawler.py` - Performance Optimization
- **Based on**: Official `arun_vs_arun_many.py`
- **Purpose**: Performance comparison and dispatcher configuration
- **Pattern**: Sequential vs parallel crawling with rate limiting
- **Features**: MemoryAdaptiveDispatcher, RateLimiter configuration
- **Usage**: `python3 advanced_concurrent_crawler.py`

## 🎯 Key Learning Outcomes

- ✅ **AsyncWebCrawler context manager** usage
- ✅ **Single URL crawling** with arun()
- ✅ **Multi-URL crawling** with arun_many()
- ✅ **Browser configuration** (headless, verbose)
- ✅ **Concurrent processing** with dispatcher
- ✅ **Performance optimization** strategies

## 📊 Performance Results

From `advanced_concurrent_crawler.py`:
- **Sequential**: 6.76 seconds
- **Parallel (with rate limit)**: 4.09 seconds  
- **Parallel (no rate limit)**: 3.95 seconds
- **Success Rate**: 100% (5/5 platforms)
- **Speed Improvement**: 71% faster with parallel processing

## 🔗 Official Documentation References

All scripts reference these official examples:
- `/workspaces/crawl4ai/docs/examples/hello_world.py`
- `/workspaces/crawl4ai/docs/examples/async_webcrawler_multiple_urls_example.py`
- `/workspaces/crawl4ai/docs/examples/extraction_strategies_examples.py`
- `/workspaces/crawl4ai/docs/examples/arun_vs_arun_many.py`

## ⚡ Quick Start

```bash
# Test basic functionality
python3 main.py

# Test single market monitoring
python3 single_market_monitor.py

# Test multi-platform crawling
python3 multi_platform_crawler.py

# Test performance optimization
python3 advanced_concurrent_crawler.py
```

## 🚀 Next Steps

Phase 1 provides the foundation. Move to:
- **Phase 2**: Real market data extraction with proper CSS selectors
- **Phase 3**: Arbitrage detection and opportunity analysis