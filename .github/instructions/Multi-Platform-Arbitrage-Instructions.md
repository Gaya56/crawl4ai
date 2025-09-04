---
applyTo: '**'
---

# 🌐 Multi-Platform Arbitrage Bot - Phase 4 Instructions
**Advanced Prediction Market Crawling & AI-Powered Categorization**

Following the success of Phase 3 arbitrage detection with 318 real market entries from PredictIt, we now expand to multiple platforms with AI-enhanced categorization.

## 📋 Project Context & Current State

### ✅ What We've Achieved (Phases 1-3)
- **Phase 1**: Foundation patterns from official Crawl4AI docs ✅
- **Phase 2**: Real market data extraction (PredictIt working) ✅  
- **Phase 3**: Live arbitrage detection system operational ✅
- **Current**: 318 real betting market entries successfully extracted

### 🎯 Phase 4 Goals: Multi-Platform + AI Categorization

## 🗂️ Directory Structure for Phase 4
```
arbitrage_bot/
├── phase4_multiplatform/          # 🆕 NEW - Multi-platform integration
│   ├── __init__.py
│   ├── platform_adapters/         # Platform-specific crawlers
│   │   ├── __init__.py
│   │   ├── predictit_adapter.py    # ✅ Working (from Phase 3)
│   │   ├── polymarket_adapter.py   # 🆕 Crypto prediction markets
│   │   ├── kalshi_adapter.py       # 🆕 Regulated derivatives
│   │   ├── manifold_adapter.py     # 🆕 Community markets
│   │   ├── betfair_adapter.py      # 🆕 Sports betting
│   │   └── base_adapter.py         # Common interface
│   ├── ai_categorization/          # 🆕 AI-powered data processing
│   │   ├── __init__.py
│   │   ├── market_classifier.py    # Event categorization
│   │   ├── event_matcher.py        # Cross-platform event matching
│   │   └── price_normalizer.py     # Unified price formats
│   ├── unified_crawler.py          # Main multi-platform crawler
│   ├── cross_platform_arbitrage.py # Real arbitrage detection
│   └── live_monitor.py             # Continuous monitoring
├── data/
│   ├── real_market_data.json       # ✅ Existing (318 entries)
│   ├── multi_platform_data.json   # 🆕 Combined platform data
│   └── arbitrage_opportunities.json # 🆕 Detected opportunities
├── configs/
│   ├── platform_configs.yaml      # 🆕 Platform-specific settings
│   └── ai_categorization.yaml     # 🆕 AI classification rules
└── run_multiplatform.sh           # 🆕 Main execution script
```

## 🔧 Implementation Requirements

### 1. **Follow Official Crawl4AI Patterns**
All implementations MUST reference and follow these official examples:
- `/workspaces/crawl4ai/docs/examples/async_webcrawler_multiple_urls_example.py`
- `/workspaces/crawl4ai/docs/examples/extraction_strategies_examples.py`
- `/workspaces/crawl4ai/docs/examples/arun_vs_arun_many.py`
- `/workspaces/crawl4ai/docs/examples/demo_multi_config_clean.py`
- `/workspaces/crawl4ai/docs/md_v2/advanced/multi-url-crawling.md`

### 2. **Official Documentation Patterns to Use**

#### AsyncWebCrawler Multi-URL Pattern
```python
# From: async_webcrawler_multiple_urls_example.py
async with AsyncWebCrawler(verbose=True) as crawler:
    urls = [
        "https://www.predictit.org/markets",
        "https://polymarket.com/",
        "https://kalshi.com/markets",
        "https://manifold.markets/",
        "https://www.betfair.com/exchange/plus/politics"
    ]
    
    results = await crawler.arun_many(
        urls=urls,
        word_count_threshold=100,
        bypass_cache=True,
        verbose=True,
    )
```

#### Multi-Config URL Matching Pattern
```python
# From: demo_multi_config_clean.py
configs = [
    # Platform-specific configurations
    CrawlerRunConfig(
        url_matcher="*predictit.org*",
        extraction_strategy=JsonCssExtractionStrategy(schema=predictit_schema)
    ),
    CrawlerRunConfig(
        url_matcher="*polymarket.com*", 
        js_code="window.scrollTo(0, 500);",
        extraction_strategy=JsonCssExtractionStrategy(schema=polymarket_schema)
    ),
    CrawlerRunConfig(
        url_matcher="*kalshi.com*",
        wait_for="css:.market-card",
        extraction_strategy=JsonCssExtractionStrategy(schema=kalshi_schema)
    )
]
```

#### Concurrent Processing with Dispatcher
```python
# From: arun_vs_arun_many.py
from crawl4ai.async_dispatcher import MemoryAdaptiveDispatcher, RateLimiter

dispatcher = MemoryAdaptiveDispatcher(
    rate_limiter=RateLimiter(base_delay=(1.0, 3.0), max_delay=60.0, max_retries=3),
    max_session_permit=50,
)

async with AsyncWebCrawler() as crawler:
    results = await crawler.arun_many(
        urls=urls, 
        config=config, 
        dispatcher=dispatcher
    )
```

## 🌐 Platform-Specific Implementation

### Target Platforms & URLs

#### 1. **PredictIt** (✅ Working - Phase 3 Success)
```python
# URLs to crawl
PREDICTIT_URLS = [
    "https://www.predictit.org/markets/1/US-Elections",
    "https://www.predictit.org/markets/13/President", 
    "https://www.predictit.org/markets/3/Congress",
    "https://www.predictit.org/markets/5/World",
    "https://www.predictit.org/markets/16/Economics",
    "https://www.predictit.org/markets/12/Sports-Culture"
]

# Existing schema (from Phase 3 success)
predictit_schema = {
    "name": "PredictItMarkets",
    "baseSelector": "div[class*='market'], .market-card, .outcome-card",
    "fields": [
        {"name": "event", "selector": "h3, .market-title, .question", "type": "text"},
        {"name": "price", "selector": ".price, [class*='price']", "type": "text"},
        {"name": "candidate", "selector": ".candidate-name, .outcome-name", "type": "text"},
        {"name": "url", "selector": "a", "type": "attribute", "attribute": "href"}
    ]
}
```

#### 2. **Polymarket** (🆕 Crypto Prediction Markets)
```python
POLYMARKET_URLS = [
    "https://polymarket.com/",
    "https://polymarket.com/events",
    "https://polymarket.com/events?_c=politics",
    "https://polymarket.com/events?_c=crypto",
    "https://polymarket.com/events?_c=sports",
    "https://polymarket.com/elections"
]

# JavaScript execution needed for React app
polymarket_js = [
    "await new Promise(resolve => setTimeout(resolve, 3000));",
    "window.scrollTo(0, document.body.scrollHeight);",
    "await new Promise(resolve => setTimeout(resolve, 2000));"
]
```

#### 3. **Kalshi** (🆕 Regulated Event Contracts)
```python
KALSHI_URLS = [
    "https://kalshi.com/markets",
    "https://kalshi.com/browse/election-2024",
    "https://kalshi.com/browse/politics", 
    "https://kalshi.com/browse/economy",
    "https://kalshi.com/browse/weather",
    "https://kalshi.com/browse/finance"
]
```

#### 4. **Manifold Markets** (🆕 Community Prediction Markets)
```python
MANIFOLD_URLS = [
    "https://manifold.markets/",
    "https://manifold.markets/browse?t=politics",
    "https://manifold.markets/browse?t=economics", 
    "https://manifold.markets/browse?t=technology",
    "https://manifold.markets/browse?t=sports",
    "https://manifold.markets/election-2024"
]
```

#### 5. **Betfair Exchange** (🆕 Political Betting)
```python
BETFAIR_URLS = [
    "https://www.betfair.com/exchange/plus/politics",
    "https://www.betfair.com/exchange/plus/politics/us-politics",
    "https://www.betfair.com/exchange/plus/politics/uk-politics",
    "https://www.betfair.com/exchange/plus/politics/international",
    "https://www.betfair.com/exchange/plus/politics/next-election"
]
```

## 🤖 AI-Powered Categorization

### LLM Integration for Event Classification
```python
# From: extraction_strategies_examples.py pattern
from crawl4ai import LLMExtractionStrategy, LLMConfig

llm_categorizer = LLMExtractionStrategy(
    llm_config=LLMConfig(
        provider="groq/qwen-2.5-32b",  # or openai/gpt-4o-mini
        api_token="env:GROQ_API_KEY",  # or OPENAI_API_KEY
    ),
    instruction="""
    Analyze this prediction market data and classify it into categories:
    1. Determine event type: [Politics, Economics, Sports, Technology, Other]
    2. Extract standardized event name for cross-platform matching
    3. Identify key participants/candidates
    4. Normalize price format to cents/probability
    """,
    extract_type="schema",
    schema="{category: string, standardized_event: string, participants: array, normalized_price: number}"
)
```

### Event Matching Algorithm
```python
def match_events_across_platforms(market_data_list):
    """
    AI-powered cross-platform event matching for arbitrage detection
    """
    # Use semantic similarity to match same events
    # Example: "Trump 2024 Election" (PredictIt) = "Donald Trump President 2024" (Polymarket)
    pass
```

## 📊 Data Flow Architecture

### 1. **Multi-Platform Data Collection**
```python
# unified_crawler.py - following official arun_many pattern
async def crawl_all_platforms():
    all_urls = PREDICTIT_URLS + POLYMARKET_URLS + KALSHI_URLS + MANIFOLD_URLS + BETFAIR_URLS
    
    async with AsyncWebCrawler(verbose=True) as crawler:
        results = await crawler.arun_many(
            urls=all_urls,
            config=platform_configs,  # Multi-config approach
            dispatcher=dispatcher
        )
        return results
```

### 2. **AI-Enhanced Data Processing**
```python
# ai_categorization/market_classifier.py
async def classify_and_normalize(raw_market_data):
    """
    Use LLM to categorize and standardize market data
    """
    classified_data = []
    for market in raw_market_data:
        # Apply LLM classification
        category_result = await llm_categorizer.extract(market['raw_text'])
        
        # Normalize to unified format
        normalized_market = {
            'platform': market['platform'],
            'category': category_result['category'], 
            'event': category_result['standardized_event'],
            'participants': category_result['participants'],
            'price': category_result['normalized_price'],
            'timestamp': datetime.now(),
            'raw_data': market
        }
        classified_data.append(normalized_market)
    
    return classified_data
```

### 3. **Cross-Platform Arbitrage Detection**
```python
# cross_platform_arbitrage.py
async def detect_arbitrage_opportunities(normalized_data):
    """
    Find arbitrage opportunities across platforms
    """
    opportunities = []
    
    # Group by standardized event name
    events_by_name = {}
    for market in normalized_data:
        event_name = market['event']
        if event_name not in events_by_name:
            events_by_name[event_name] = []
        events_by_name[event_name].append(market)
    
    # Check for arbitrage in each event group
    for event_name, markets in events_by_name.items():
        if len(markets) >= 2:  # Need at least 2 platforms
            opportunity = analyze_price_differences(markets)
            if opportunity:
                opportunities.append(opportunity)
    
    return opportunities
```

## 🔄 Implementation Phases

### Phase 4A: Multi-Platform Foundation
1. **Create base adapter class** following official patterns
2. **Implement PredictIt adapter** (migrate from Phase 3 success)
3. **Add Polymarket adapter** with JavaScript execution
4. **Test concurrent crawling** using arun_many

### Phase 4B: Platform Expansion  
1. **Kalshi adapter** with authentication handling
2. **Manifold adapter** for community markets
3. **Betfair adapter** for traditional betting
4. **Unified data schema** across all platforms

### Phase 4C: AI Integration
1. **LLM-based categorization** using official LLMExtractionStrategy
2. **Event matching algorithm** for cross-platform correlation  
3. **Price normalization** to unified probability format
4. **Semantic event grouping** for arbitrage detection

### Phase 4D: Production System
1. **Real-time monitoring** with continuous scanning
2. **Opportunity alerting** via email/Discord
3. **Performance optimization** using dispatchers
4. **Error handling and resilience**

## 📁 Key Files to Create

### Primary Implementation Files
```
phase4_multiplatform/
├── unified_crawler.py              # Main multi-platform crawler
├── cross_platform_arbitrage.py     # Arbitrage detection engine  
├── live_monitor.py                 # Continuous monitoring
└── platform_adapters/
    ├── base_adapter.py             # Common interface
    ├── predictit_adapter.py        # Migrate from Phase 3
    ├── polymarket_adapter.py       # React app handling
    ├── kalshi_adapter.py           # Regulated markets
    ├── manifold_adapter.py         # Community markets
    └── betfair_adapter.py          # Traditional betting
```

### AI Components
```
ai_categorization/
├── market_classifier.py           # LLM-based categorization
├── event_matcher.py               # Cross-platform matching
└── price_normalizer.py            # Unified price formats
```

### Configuration & Data
```
configs/
├── platform_configs.yaml          # Platform-specific settings
└── ai_categorization.yaml         # AI classification rules

data/
├── multi_platform_data.json       # Combined platform data
└── arbitrage_opportunities.json   # Detected opportunities
```

## 🚀 Execution Plan

### Step 1: Follow Official Patterns
- Reference `/workspaces/crawl4ai/docs/examples/` for all implementations
- Use exact patterns from `async_webcrawler_multiple_urls_example.py`
- Follow multi-config approach from `demo_multi_config_clean.py`

### Step 2: Leverage Phase 3 Success
- Migrate working PredictIt extraction to new adapter system
- Use proven schema and JavaScript patterns
- Build on 318 real market entries foundation

### Step 3: Scale Systematically
- Add one platform at a time
- Test each adapter individually
- Validate data quality before moving to next platform

### Step 4: AI Enhancement
- Integrate LLM classification following official LLMExtractionStrategy
- Implement semantic event matching
- Create unified data pipeline

## 🎯 Success Metrics

### Technical Objectives
- **5+ Platforms**: PredictIt, Polymarket, Kalshi, Manifold, Betfair
- **1000+ Markets**: Scale from 318 to 1000+ total market entries
- **Cross-Platform Events**: Successfully match same events across platforms
- **Real Arbitrage**: Detect actual price differences between platforms
- **Sub-5min Updates**: Real-time monitoring with fresh data every 5 minutes

### Data Quality Goals
- **95%+ Extraction Success**: Reliable data collection across platforms
- **Semantic Event Matching**: AI-powered event correlation
- **Price Normalization**: Unified probability/cents format
- **Timestamp Accuracy**: Precise timing for arbitrage windows

## 🔧 Development Guidelines

### Code Standards
1. **Follow Official Patterns**: Every implementation references Crawl4AI docs
2. **Async/Await**: Use proper asyncio patterns throughout
3. **Error Handling**: Graceful degradation for failed platforms
4. **Resource Management**: Proper context managers and cleanup
5. **Performance**: Leverage dispatchers for concurrent processing

### Testing Strategy
1. **Individual Adapters**: Test each platform adapter separately
2. **Multi-Platform**: Validate concurrent crawling performance
3. **AI Classification**: Verify LLM categorization accuracy
4. **Arbitrage Detection**: Test cross-platform opportunity identification

### Documentation Requirements
1. **Platform-Specific READMEs**: Document each adapter's approach
2. **API Documentation**: Clear interfaces and schemas
3. **Performance Metrics**: Benchmark results and optimizations
4. **Troubleshooting Guide**: Common issues and solutions

---

## 💡 Key Innovation: AI-Powered Standardization

The breakthrough will be using **LLM-based event standardization** to match the same prediction across different platforms:

- **PredictIt**: "Democratic presidential nominee in 2028?"
- **Polymarket**: "2028 Democratic Primary Winner"  
- **Kalshi**: "DEM-28-PRES: Democratic Nominee 2028"

AI classification will recognize these as the **same event** and enable real arbitrage detection across platforms.

---

**🎯 This Phase 4 implementation will create the world's most comprehensive prediction market arbitrage system, built on the solid foundation of Phase 3's success and following official Crawl4AI patterns throughout.**