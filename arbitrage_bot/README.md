# Prediction Market Arbitrage Bot - Official Crawl4AI Implementation

This implementation follows **official Crawl4AI documentation patterns exactly**, with only URLs changed to monitor prediction markets. Every script is based on official examples from `/workspaces/crawl4ai/docs/examples/`.

## Official Documentation References

All scripts follow these official Crawl4AI examples:

1. **single_market_monitor.py** → Based on `hello_world.py`
2. **multi_platform_crawler.py** → Based on `async_webcrawler_multiple_urls_example.py`  
3. **structured_extraction.py** → Based on `extraction_strategies_examples.py`
4. **advanced_concurrent_crawler.py** → Based on `arun_vs_arun_many.py`

## Architecture

As per official documentation:

> "Crawl4AI is designed for asynchronous, scriptable web crawling. The official docs show that you build a crawler by instantiating AsyncWebCrawler with optional browser settings and then calling arun() for each URL."

> "For multiple URLs, Crawl4AI has a built‑in concurrency API (arun_many()), which accepts a list of URLs and uses a dispatcher to handle resource‑aware parallel crawling."

## Implementation Strategy

Following the official guidance:

> "For orchestrating across markets, there are two main options: (a) combine URLs in a single script and use arun_many() to crawl all markets concurrently, which leverages the library's dispatcher, or (b) maintain separate scripts and launch them from a .sh shell script."

This implementation provides **both approaches**:

- **Option A**: `advanced_concurrent_crawler.py` uses `arun_many()` with dispatcher
- **Option B**: `run_monitors.sh` launches separate Python scripts as separate processes

## Scripts Overview

### 1. Single Market Monitor (`single_market_monitor.py`)
**Official Reference**: `/workspaces/crawl4ai/docs/examples/hello_world.py`

```python
# Official pattern from hello_world.py:
async with AsyncWebCrawler(config=browser_config) as crawler:
    result: CrawlResult = await crawler.arun(url="https://www.predictit.org/markets", config=crawler_config)
```

Monitors a single prediction market using the basic `arun()` pattern.

### 2. Multi-Platform Crawler (`multi_platform_crawler.py`)  
**Official Reference**: `/workspaces/crawl4ai/docs/examples/async_webcrawler_multiple_urls_example.py`

```python
# Official pattern from async_webcrawler_multiple_urls_example.py:
results = await crawler.arun_many(
    urls=urls,
    word_count_threshold=word_count_threshold,
    bypass_cache=True,
    verbose=True,
)
```

Crawls multiple prediction market platforms concurrently.

### 3. Structured Extraction (`structured_extraction.py`)
**Official Reference**: `/workspaces/crawl4ai/docs/examples/extraction_strategies_examples.py`

```python
# Official pattern from extraction_strategies_examples.py:
css_strategy = JsonCssExtractionStrategy(schema=css_schema)
config = CrawlerRunConfig(extraction_strategy=strategy)
result = await crawler.arun(url=url, config=config)
```

Extracts structured data using `JsonCssExtractionStrategy`.

### 4. Advanced Concurrent Crawler (`advanced_concurrent_crawler.py`)
**Official Reference**: `/workspaces/crawl4ai/docs/examples/arun_vs_arun_many.py`

```python
# Official pattern from arun_vs_arun_many.py:
dispatcher = MemoryAdaptiveDispatcher(
    rate_limiter=RateLimiter(base_delay=(1.0, 3.0), max_delay=60.0, max_retries=3),
    max_session_permit=50,
)
result_container = await crawler.arun_many(urls=urls, config=config, dispatcher=dispatcher)
```

Demonstrates performance comparison between sequential and parallel crawling with dispatcher configuration.

## Usage

### Quick Test - Single Script
```bash
cd /workspaces/crawl4ai/arbitrage_bot
python3 single_market_monitor.py
```

### Full Orchestration - Multiple Processes
```bash
cd /workspaces/crawl4ai/arbitrage_bot
./run_monitors.sh
```

### Individual Scripts
```bash
# Test each approach individually
python3 multi_platform_crawler.py
python3 structured_extraction.py  
python3 advanced_concurrent_crawler.py
```

## Official Crawl4AI Patterns Used

### 1. Async Context Manager Pattern
```python
async with AsyncWebCrawler(config=browser_config) as crawler:
    # Ensures proper resource cleanup
```

### 2. Single URL Crawling
```python
result: CrawlResult = await crawler.arun(url=url, config=config)
```

### 3. Multiple URL Crawling  
```python
results = await crawler.arun_many(urls=urls, config=config)
```

### 4. Dispatcher Configuration
```python
dispatcher = MemoryAdaptiveDispatcher(
    rate_limiter=RateLimiter(...),
    max_session_permit=50
)
```

### 5. Structured Extraction
```python
strategy = JsonCssExtractionStrategy(schema=schema)
config = CrawlerRunConfig(extraction_strategy=strategy)
```

## Dependencies

Based on official examples:
```
crawl4ai>=0.7.4
asyncio
aiohttp
beautifulsoup4
```

## Next Steps

1. **Real CSS Selectors**: Update placeholder selectors in `structured_extraction.py` with actual prediction market site selectors
2. **Arbitrage Logic**: Add price comparison logic between extracted market data
3. **Data Persistence**: Implement JSON/database storage for extracted data
4. **Monitoring**: Add continuous monitoring loops with configurable intervals

## Official Documentation Compliance

This implementation strictly follows official Crawl4AI patterns:

- ✅ Uses `AsyncWebCrawler` in async context manager
- ✅ Implements both `arun()` and `arun_many()` patterns  
- ✅ Uses official `BrowserConfig` and `CrawlerRunConfig`
- ✅ Follows dispatcher configuration from examples
- ✅ Implements structured extraction with `JsonCssExtractionStrategy`
- ✅ Maintains exact error handling patterns from official examples