---
applyTo: '**'
---

# 🎯 Crawl4AI Project Instructions

## 📋 Current Project Status

### ✅ Completed: Prediction Market Arbitrage Bot (Phases 1-3)
**Location**: `/workspaces/crawl4ai/arbitrage_bot/`
**Status**: Fully operational arbitrage detection system
**Achievement**: 318 real market entries extracted from PredictIt

### 🚀 Next Phase: Multi-Platform Expansion (Phase 4)
**Instruction File**: `/workspaces/crawl4ai/.github/instructions/Multi-Platform-Arbitrage-Instructions.md`
**Goal**: Scale to 5+ platforms with AI-powered event matching

---

## 🔧 Development Guidelines

### 1. **Official Documentation First**
ALWAYS reference official Crawl4AI examples from:
- `/workspaces/crawl4ai/docs/examples/`
- `/workspaces/crawl4ai/docs/md_v2/`
- Follow exact patterns from `async_webcrawler_multiple_urls_example.py`
- Use `demo_multi_config_clean.py` for multi-platform configurations
- Reference `arun_vs_arun_many.py` for performance optimization

### 2. **Proven Patterns to Follow**
```python
# AsyncWebCrawler Context Manager Pattern
async with AsyncWebCrawler(verbose=True) as crawler:
    results = await crawler.arun_many(urls=urls, config=config)

# Multi-Config URL Matching Pattern  
configs = [
    CrawlerRunConfig(url_matcher="*predictit.org*", extraction_strategy=strategy1),
    CrawlerRunConfig(url_matcher="*polymarket.com*", js_code="window.scrollTo(0, 500);"),
]

# Concurrent Processing with Dispatcher
from crawl4ai.async_dispatcher import MemoryAdaptiveDispatcher, RateLimiter
dispatcher = MemoryAdaptiveDispatcher(rate_limiter=RateLimiter(...))
```

### 3. **Current Working Foundation**
- **Phase 3 Success**: PredictIt extraction working with 318 real entries
- **Proven JavaScript**: Dynamic content handling for React apps
- **Arbitrage Engine**: Price parsing and opportunity detection operational
- **Performance**: 71% improvement with concurrent crawling

### 4. **Target Platforms for Expansion**
- **PredictIt**: ✅ Working (Phase 3 success)
- **Polymarket**: 🆕 Crypto prediction markets (React app)
- **Kalshi**: 🆕 Regulated event contracts
- **Manifold**: 🆕 Community prediction markets  
- **Betfair**: 🆕 Political betting exchange

### 5. **AI Integration Requirements**
- Use `LLMExtractionStrategy` for event categorization
- Implement semantic event matching across platforms
- Normalize price formats (cents/probability)
- Enable cross-platform arbitrage detection

---

## 📁 Project Structure Reference

### Current Working System
```
arbitrage_bot/
├── phase3_arbitrage/           # ✅ Working arbitrage detection
├── phase2_extraction/          # ✅ PredictIt data extraction
├── phase1_foundation/          # ✅ All official patterns
├── data/real_market_data.json  # ✅ 318 real market entries
└── run_monitors.sh             # ✅ Phase 3 execution
```

### Next Implementation (Phase 4)
```
phase4_multiplatform/
├── platform_adapters/          # Platform-specific crawlers
├── ai_categorization/          # LLM-based event matching
├── unified_crawler.py          # Multi-platform coordination
└── cross_platform_arbitrage.py # Real arbitrage detection
```

---

## 🎯 When Working on This Project

1. **Start with Official Examples**: Always check docs/examples/ first
2. **Build on Phase 3 Success**: Leverage working PredictIt patterns
3. **Follow Multi-Config Approach**: Use URL matchers for different platforms
4. **Use Proven JavaScript**: Apply dynamic content handling patterns
5. **Implement AI Categorization**: LLM-based event standardization
6. **Focus on Real Arbitrage**: Cross-platform price difference detection

### Success Metrics
- **5+ Platforms**: Scale beyond PredictIt to full ecosystem
- **1000+ Markets**: Grow from 318 to 1000+ market entries
- **Real Opportunities**: Detect actual arbitrage across platforms
- **Sub-5min Updates**: Real-time monitoring capabilities

---

**💡 Key Innovation**: AI-powered event standardization to match same predictions across different platforms for true arbitrage detection.

**📖 Complete Instructions**: See `Multi-Platform-Arbitrage-Instructions.md` for detailed implementation guide.