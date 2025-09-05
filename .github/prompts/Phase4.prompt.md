---
mode: agent
---

# 🚀 Crawl4AI Multi-Platform Arbitrage Bot - Phase 4 Implementation

## 📋 Project Context & Summary

This prompt launches Phase 4 of the comprehensive Crawl4AI arbitrage bot project: **Multi-Platform Expansion with AI-Powered Event Categorization**. Following a successful baseline review that confirmed our operational system with 318 real market entries from PredictIt, we now implement platform-specific adapters and AI-enhanced event matching across 5+ prediction market platforms. All implementations will strictly follow official Crawl4AI patterns with stepwise validation and clear documentation citations.

## 🎯 Expert AI Developer Role

You are an expert AI developer-assistant working in a Crawl4AI-compatible environment. Your goal is to implement Phase 4 of our arbitrage bot: expanding from our working PredictIt foundation to multiple prediction market platforms with AI-powered event categorization for cross-platform arbitrage detection. Proceed one small step at a time with clear checkpoints, summaries, and citations to official Crawl4AI patterns.

## 📁 Scope and Sources to Use

### Primary Local Code Base
- **Main System**: `/workspaces/crawl4ai/arbitrage_bot/` 
  - `phase3_arbitrage/` - ✅ Working arbitrage detection (318 real entries)
  - `phase2_extraction/` - ✅ PredictIt data extraction  
  - `phase1_foundation/` - ✅ All official patterns implemented
- **Instructions**: `/workspaces/crawl4ai/.github/instructions/`
  - `Multi-Platform-Arbitrage-Instructions.md` - Complete Phase 4 specifications
  - `Next-step.instructions.md` - Project context and guidelines

### Reference Implementation Patterns (Required Sources)
- **Local Official Examples**: `/workspaces/crawl4ai/docs/examples/`
  - `async_webcrawler_multiple_urls_example.py` - Multi-URL concurrent crawling
  - `demo_multi_config_clean.py` - URL matching with platform-specific configs
  - `extraction_strategies_examples.py` - LLM and JSON extraction strategies
  - `arun_vs_arun_many.py` - Performance optimization with dispatchers
- **Local Documentation**: `/workspaces/crawl4ai/docs/md_v2/`
- **External References** (only as backup):
  - Official Crawl4AI repository: https://github.com/unclecode/crawl4ai
  - Official documentation: https://docs.crawl4ai.com

## 🛠️ MCP Tools Available

- **mcp_filesystem_***: Explore, read, write, and analyze workspace files
- **mcp_pylance_***: Python type analysis, error detection, syntax validation, refactoring
- **mcp_brave-search_***: Retrieve official documentation (only if local sources insufficient)  
- **mcp_memory_***: Track decisions, conventions, patterns, and lessons learned
- **mcp_sequential-th_***: Complex problem analysis and planning

## ⚙️ Operating Principles

### Iterative Development Standards
- **One small step at a time** with explicit validation points
- After each step provide:
  - Short summary of changes and rationale
  - Minimal checklist of completed and next tasks  
  - Exact code lines changed with official source citations
  - Reference to specific official pattern followed

### Code Modification Standards
- **Copy canonical patterns** from local official examples first (`/workspaces/crawl4ai/docs/examples/`)
- Adapt to our arbitrage bot structure with clear citations
- Prefer small, reversible changes (split large changes into steps)
- Always include exact file paths and line numbers for changes

### Reference Requirements
- **Code references**: Exact local file paths (`/workspaces/crawl4ai/docs/examples/file.py:line`)
- **Documentation**: Specific sections from local docs first
- **External sources**: Only when local sources insufficient, with full URLs

### Safety and Quality Standards
- **Pylance validation** before committing any changes
- **Type safety** throughout the codebase
- **Local testing** when feasible for each change
- **Official pattern compliance** for all implementations

### Memory Management
- Track: Linting rules, structure decisions, naming patterns, error handling
- Record: Common pitfalls and solutions
- Maintain: Consistent conventions across all steps

## 🎯 Phase 4 Implementation Plan

### ✅ Step 1: Multi-Config URL Matching Implementation
**Goal**: Update `phase1_foundation/multi_platform_crawler.py` to use CrawlerRunConfig with platform-specific URL matchers following official patterns.

**Official Reference**: `/workspaces/crawl4ai/docs/examples/demo_multi_config_clean.py`

**Implementation Pattern**:
```python
# From demo_multi_config_clean.py - URL matching with configs
configs = [
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
        wait_for="css:.market-card"
    )
]
```

**Validation**: Pylance check + dry-run to confirm platform-specific configurations work correctly.

### 🔄 Step 2: Platform Adapter Architecture
**Goal**: Create `phase4_multiplatform/platform_adapters/` directory structure with base adapter interface.

**Official Reference**: `/workspaces/crawl4ai/docs/examples/extraction_strategies_examples.py` for extraction strategy patterns.

### 🤖 Step 3: AI-Powered Event Classification  
**Goal**: Implement LLM-based event categorization using official LLMExtractionStrategy patterns.

**Official Reference**: `/workspaces/crawl4ai/docs/examples/extraction_strategies_examples.py` - LLM extraction patterns.

### 🌐 Step 4: Multi-Platform Data Collection
**Goal**: Implement unified crawler using arun_many with dispatcher for concurrent processing.

**Official Reference**: `/workspaces/crawl4ai/docs/examples/arun_vs_arun_many.py` for performance optimization.

### 💰 Step 5: Cross-Platform Arbitrage Detection
**Goal**: Build arbitrage detection engine that processes normalized data from multiple platforms.

## 📊 Target Platform Integration

### Platform URLs and Configurations
Based on Phase 4 instructions and proven patterns:

```python
# Platform-specific URL patterns
PLATFORM_URLS = {
    "predictit": [
        "https://www.predictit.org/markets/21/Elections",
        "https://www.predictit.org/markets/3/President", 
        "https://www.predictit.org/markets/2/Congress"
    ],
    "polymarket": [
        "https://polymarket.com/events?_c=politics",
        "https://polymarket.com/events?_c=crypto",
        "https://polymarket.com/elections"
    ],
    "kalshi": [
        "https://kalshi.com/browse/election-2024",
        "https://kalshi.com/browse/politics",
        "https://kalshi.com/browse/economy"
    ],
    "manifold": [
        "https://manifold.markets/browse?t=politics",
        "https://manifold.markets/browse?t=economics",
        "https://manifold.markets/election-2024"
    ],
    "betfair": [
        "https://www.betfair.com/exchange/plus/politics/us-politics",
        "https://www.betfair.com/exchange/plus/politics/uk-politics"
    ]
}
```

## 🔧 Implementation Guidelines

### Code Standards
1. **Follow Official Patterns**: Every implementation references local Crawl4AI examples
2. **AsyncWebCrawler Context Manager**: Proper resource management pattern
3. **Multi-Config Approach**: Use URL matchers for platform-specific handling
4. **Performance Optimization**: Leverage dispatchers for concurrent processing
5. **Type Safety**: Full Pylance validation throughout

### File Creation Strategy
1. **Migrate Working Code**: Move Phase 3 PredictIt success to new adapter system
2. **Incremental Platform Addition**: Add one platform at a time with validation
3. **AI Integration**: Implement LLM categorization following official strategies
4. **Unified Pipeline**: Create cross-platform data flow with arbitrage detection

### Testing and Validation
1. **Pylance Checks**: Type validation after each change
2. **Individual Platform Tests**: Validate each adapter separately  
3. **Multi-Platform Integration**: Test concurrent crawling performance
4. **AI Classification**: Verify LLM categorization accuracy

## 🚧 Constraints and Safety Measures

### Pattern Fidelity
- **No invention**: Only use patterns from official sources with citations
- **Local examples first**: Prefer `/workspaces/crawl4ai/docs/examples/` over external docs
- **Small steps**: Split large changes into validated increments
- **Working foundation**: Build on Phase 3's proven 318-entry success

### Quality Assurance
- **Traceability**: All changes link to official pattern sources
- **Type Safety**: Pylance validation shows improvement progressively  
- **Functionality**: Arbitrage bot remains operational throughout development
- **Documentation**: Each step includes citations and next-step planning

## 📦 Expected Deliverables

### File Structure After Phase 4
```
arbitrage_bot/
├── phase4_multiplatform/           # 🆕 Multi-platform integration
│   ├── platform_adapters/          # Platform-specific crawlers
│   │   ├── base_adapter.py         # Common interface
│   │   ├── predictit_adapter.py    # Migrated from Phase 3
│   │   ├── polymarket_adapter.py   # React app handling
│   │   ├── kalshi_adapter.py       # Regulated markets
│   │   ├── manifold_adapter.py     # Community markets
│   │   └── betfair_adapter.py      # Traditional betting
│   ├── ai_categorization/          # AI-powered processing
│   │   ├── market_classifier.py    # Event categorization
│   │   ├── event_matcher.py        # Cross-platform matching
│   │   └── price_normalizer.py     # Unified price formats
│   ├── unified_crawler.py          # Multi-platform crawler
│   ├── cross_platform_arbitrage.py # Arbitrage detection
│   └── live_monitor.py             # Continuous monitoring
├── data/
│   ├── multi_platform_data.json   # Combined platform data
│   └── arbitrage_opportunities.json # Detected opportunities
└── run_multiplatform.sh           # Main execution script
```

### Success Metrics
- **5+ Platforms**: PredictIt, Polymarket, Kalshi, Manifold, Betfair
- **1000+ Markets**: Scale from 318 to 1000+ total market entries
- **AI Event Matching**: Cross-platform event correlation working
- **Real Arbitrage**: Actual price differences detected between platforms
- **Performance**: Sub-5 minute update cycles with concurrent processing

## 🏁 Acceptance Criteria

### Technical Requirements
- **Official Pattern Compliance**: All code follows local Crawl4AI examples
- **Type Safety**: Clean Pylance validation throughout
- **Performance**: Leverages dispatchers for optimal concurrent crawling  
- **AI Integration**: Working LLM categorization using official strategies
- **Cross-Platform Data**: Unified schema across all platforms

### Operational Requirements  
- **Maintains Phase 3 Success**: PredictIt extraction continues working
- **Scalable Architecture**: Easy addition of new platforms
- **Error Resilience**: Graceful handling of platform failures
- **Real-Time Capability**: Foundation for continuous monitoring

---

## 🚀 EXECUTE: Start with Step 1

**Instructions**: Begin with Step 1 (Multi-Config URL Matching Implementation) following the stepwise format. Update `phase1_foundation/multi_platform_crawler.py` to use the official `demo_multi_config_clean.py` patterns. Provide clear citations, validate with Pylance, and prepare for Step 2.

**Focus**: Build on our working Phase 3 foundation (318 real market entries) while implementing official Crawl4AI multi-config patterns for Phase 4 multi-platform expansion.