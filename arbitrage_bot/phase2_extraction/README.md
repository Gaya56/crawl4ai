# Phase 2: Market Data Extraction - Real Betting Data

This directory contains scripts that extract actual market data from prediction market platforms.

## 📁 Scripts Overview

### `phase2_market_data_extraction.py` - Structure Analysis
- **Purpose**: Analyze page structures and understand HTML layouts
- **Method**: Broad CSS selectors to capture various data elements
- **Output**: Inspects page structure to identify potential market data
- **Platforms**: PredictIt, Polymarket, Kalshi
- **Usage**: `python3 phase2_market_data_extraction.py`

### `phase2b_advanced_extraction.py` - Dynamic Content Extraction
- **Purpose**: Extract market data with JavaScript execution
- **Method**: Uses js_code and wait_for parameters for dynamic content
- **Features**: 
  - JavaScript execution for React/dynamic apps
  - Targeted market URLs (not just homepages)
  - Wait conditions for content loading
- **Success**: Successfully extracts PredictIt election data
- **Usage**: `python3 phase2b_advanced_extraction.py`

## 🎯 Key Breakthroughs

### ✅ Real Market Data Extracted
From PredictIt Elections:
```
Event: "Democratic presidential nominee in 2028?"
Candidate: "Gavin Newsom"
Price: 34¢ (34 cents)
Volume: "390K Shares Traded"
Market Link: /markets/detail/8153/Who-will-win-the-2028-Democratic-presidential-nomination
```

### 📊 Extraction Results
- **PredictIt**: ✅ 162 market items successfully extracted
- **Polymarket**: ❌ Timeout (requires better selectors)
- **Kalshi**: ❌ Minimal content (needs authentication/specific URLs)

## 🔧 Technical Approach

### CSS Selectors Used
```python
schema = {
    "name": "PredictItElections", 
    "baseSelector": "div[class*='market'], article, .card",
    "fields": [
        {"name": "title", "selector": "h1, h2, h3, .title", "type": "text"},
        {"name": "yes_price", "selector": ".yes, [class*='yes']", "type": "text"},
        {"name": "no_price", "selector": ".no, [class*='no']", "type": "text"},
        {"name": "all_prices", "selector": "[class*='price'], .price", "type": "text"}
    ]
}
```

### JavaScript Execution
```python
js_code = [
    "await new Promise(resolve => setTimeout(resolve, 3000));",
    "window.scrollTo(0, document.body.scrollHeight);",
    "await new Promise(resolve => setTimeout(resolve, 2000));"
]
```

## 📈 Data Quality

### Successful Extraction Pattern
```json
{
  "title": "Democratic presidential nominee in 2028?",
  "yes_price": null,
  "no_price": "Gavin Newsom34¢1¢A. Ocasio-Cortez11¢NC390KSharesTraded",
  "all_prices": "34¢",
  "links": "/markets/detail/8153/Who-will-win-the-2028-Democratic-presidential-nomination"
}
```

## 🚧 Current Challenges

### PredictIt ✅ WORKING
- Successfully extracting prices and market data
- Need better parsing for individual candidates
- Volume data available

### Polymarket ❌ NEEDS WORK  
- Timeout waiting for selectors
- Requires React app loading
- Need different wait conditions

### Kalshi ❌ NEEDS WORK
- Very minimal content returned
- May require authentication
- Need specific market URLs

## 🔄 Improvement Areas

1. **Better CSS Selectors**: Inspect actual HTML for precise selectors
2. **Enhanced JavaScript**: More sophisticated dynamic content handling  
3. **Error Handling**: Graceful fallbacks for failed extractions
4. **Platform-Specific Logic**: Tailored approaches for each platform

## ⚡ Quick Start

```bash
# Analyze page structures
python3 phase2_market_data_extraction.py

# Extract with JavaScript (recommended)
python3 phase2b_advanced_extraction.py
```

## 🚀 Next Steps

Phase 2 successfully extracts real market data from PredictIt. Ready for:
- **Phase 3**: Process this data for arbitrage detection
- **Multi-Platform**: Improve Polymarket and Kalshi extraction
- **Real-Time**: Continuous monitoring for live opportunities