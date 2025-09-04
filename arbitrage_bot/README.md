# 🚀 Prediction Market Arbitrage Bot

A complete arbitrage bot for prediction markets built with **Crawl4AI** - the #1 trending GitHub web crawler. This bot monitors multiple prediction market platforms, identifies arbitrage opportunities, and sends real-time notifications for profitable trades.

## 🎯 What is Prediction Market Arbitrage?

Arbitrage in prediction markets involves capitalizing on price discrepancies across different platforms for the same event. The bot identifies two main types of opportunities:

1. **Direct Price Arbitrage**: Same outcome priced differently on different platforms (buy low, sell high)
2. **Complementary Arbitrage**: When Yes + No prices for the same event sum to less than $1.00 (guaranteed profit)

## ✨ Features

- 🌐 **Multi-Platform Crawling**: Concurrent crawling of multiple prediction market sites
- 🧠 **Smart Arbitrage Detection**: Identifies both direct and complementary arbitrage opportunities  
- 🚨 **Real-Time Alerts**: Instant notifications when profitable opportunities are found
- 💾 **Data Persistence**: Stores market data and opportunities for analysis
- 🔄 **Automated Monitoring**: Continuous background monitoring with configurable intervals
- 📊 **Performance Tracking**: Tracks opportunities found and alerts sent
- 🛡️ **Error Handling**: Robust error handling for reliable operation

## 🏗️ Project Structure

```
arbitrage_bot/
├── complete_arbitrage_bot.py      # Main production-ready bot
├── main.py                        # Phase 1: Single-source extraction
├── phase2_multi_platform.py       # Phase 2: Multi-platform crawling
├── phase3_arbitrage_detection.py  # Phase 3: Arbitrage logic
├── phase4_automation.py           # Phase 4: Automation & monitoring
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── market_data_*.json            # Stored market data
├── arbitrage_opportunities_*.json # Found opportunities
└── arbitrage_alerts.log          # Alert history
```

## 🚀 Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set up Crawl4AI browser components
crawl4ai-setup
```

### 2. Run the Complete Bot

```bash
python complete_arbitrage_bot.py
```

### 3. Test Individual Phases

```bash
# Test single-source extraction
python main.py

# Test multi-platform crawling
python phase2_multi_platform.py

# Test arbitrage detection
python phase3_arbitrage_detection.py

# Test automated monitoring
python phase4_automation.py
```

## 🔧 Configuration

### Market Configuration

Update the `market_configs` in `complete_arbitrage_bot.py` to add new prediction market sites:

```python
self.market_configs = {
    "predictit": {
        "url": "https://www.predictit.org/markets",
        "schema": {
            "name": "PredictItMarkets",
            "baseSelector": ".market-card",
            "fields": [
                {"name": "event_title", "selector": ".market-title", "type": "text"},
                {"name": "yes_price", "selector": ".yes-price", "type": "text"},
                # Add more fields as needed
            ]
        }
    }
    # Add more markets...
}
```

### Monitoring Settings

```python
await bot.start_monitoring(
    max_cycles=100,        # Number of monitoring cycles
    sleep_interval=300,    # 5 minutes between cycles
    use_mock_data=False    # Set to True for testing
)
```

## 📊 Example Output

```
🤖 Starting Prediction Market Arbitrage Bot
   📊 Max monitoring cycles: 3
   ⏰ Sleep interval: 10 seconds
   🌐 Using mock data: True

🔄 Running monitoring cycle at 2025-09-04 21:04:25
🌐 Crawling prediction market sites...
📊 Collected data from 4 sources
🔍 Analyzing market data for arbitrage opportunities...
🎯 Found 2 arbitrage opportunities

🚨 ARBITRAGE OPPORTUNITY DETECTED! 🚨

Event: Bitcoin to reach $150k in 2025
Type: Direct Price Arbitrage
Outcome: Yes
Sources: PredictIt, Polymarket
Strategy: Buy at $0.28, sell at $0.35
Profit Potential: 25.00%
Detected: 2025-09-04T21:04:25.123456

Take action quickly - arbitrage opportunities disappear fast!
```

## 🔍 How It Works

### Phase 1: Single-Source Data Extraction
- Tests extraction on a known website (Hacker News)
- Validates CSS selector schemas
- Ensures the crawling approach works

### Phase 2: Multi-Platform Price Aggregation  
- Crawls multiple URLs concurrently using `arun_many()`
- Applies different extraction schemas per platform
- Aggregates pricing data from all sources

### Phase 3: Arbitrage Detection & Data Persistence
- Normalizes event titles for cross-platform matching
- Implements arbitrage detection algorithms
- Stores data in JSON files (ready for database integration)

### Phase 4: Automation & Continuous Monitoring
- Automated monitoring loops with configurable intervals
- Real-time notification system
- Error handling and logging

## 🛠️ Technical Implementation

### Built with Crawl4AI Features

- **JsonCssExtractionStrategy**: Fast, LLM-free data extraction using CSS selectors
- **Multi-URL Configuration**: Different schemas for different platforms
- **Concurrent Crawling**: Parallel processing with `arun_many()`
- **Browser Management**: Handles JavaScript-heavy prediction market sites
- **Caching**: Avoids redundant requests

### Arbitrage Detection Algorithm

```python
# Direct Price Arbitrage
if max_price > min_price:
    profit_per_share = max_price - min_price
    profit_percentage = (profit_per_share / min_price) * 100

# Complementary Arbitrage  
if yes_price + no_price < 1.0:
    guaranteed_profit = 1.0 - (yes_price + no_price)
    profit_percentage = (guaranteed_profit / (yes_price + no_price)) * 100
```

## 🚀 Production Deployment

### 1. Database Integration (Supabase)

```python
from supabase import create_client

supabase = create_client("YOUR_SUPABASE_URL", "YOUR_SUPABASE_KEY")

# Store market data
supabase.table('market_data').insert(market_data).execute()

# Store opportunities
supabase.table('arbitrage_opportunities').insert(opportunities).execute()
```

### 2. Real-Time Notifications

```python
# Slack integration
import requests

def send_slack_alert(opportunity):
    webhook_url = "YOUR_SLACK_WEBHOOK_URL"
    payload = {
        "text": f"🚨 Arbitrage Alert: {opportunity['event_title']} - {opportunity['profit_percentage']:.2f}% profit!"
    }
    requests.post(webhook_url, json=payload)
```

### 3. Cloud Deployment

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN crawl4ai-setup

COPY . .
CMD ["python", "complete_arbitrage_bot.py"]
```

### 4. Monitoring & Scaling

- Deploy with Docker on AWS/GCP/Azure
- Use cron jobs or cloud schedulers for automation
- Implement rate limiting to respect site ToS
- Add monitoring with Prometheus/Grafana

## 📈 Performance & Scalability

- **Concurrent Crawling**: Process multiple sites simultaneously
- **Efficient Extraction**: CSS selectors avoid expensive LLM calls
- **Smart Caching**: Reduce redundant requests
- **Configurable Intervals**: Balance speed vs. respectful crawling

## ⚖️ Legal & Ethical Considerations

- **Terms of Service**: Ensure compliance with each platform's ToS
- **Rate Limiting**: Implement respectful crawling practices
- **Data Usage**: Use extracted data only for personal arbitrage
- **Risk Management**: Understand that arbitrage opportunities carry execution risk

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add new prediction market integrations
4. Improve arbitrage detection algorithms
5. Submit a pull request

## 📝 License

This project is for educational purposes. Please ensure compliance with all applicable laws and terms of service when using prediction market data.

## 🙏 Acknowledgments

- **Crawl4AI**: Powering the web crawling infrastructure
- **Prediction Markets**: For providing valuable market data
- **Open Source Community**: For making projects like this possible

---

**⚠️ Disclaimer**: This bot is for educational purposes. Prediction market arbitrage involves financial risk. Always do your own research and never invest more than you can afford to lose.

## 🔗 Learn More

- [Crawl4AI Documentation](https://docs.crawl4ai.com/)
- [Prediction Market Theory](https://en.wikipedia.org/wiki/Prediction_market)
- [Arbitrage Strategies](https://en.wikipedia.org/wiki/Arbitrage)

---

Built with ❤️ using [Crawl4AI](https://github.com/unclecode/crawl4ai) - The #1 Trending GitHub Web Crawler