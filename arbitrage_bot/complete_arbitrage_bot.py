import asyncio
import json
import os
from datetime import datetime
from typing import List, Dict, Any

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai import JsonCssExtractionStrategy

class PredictionMarketArbitrageBot:
    """
    Complete Prediction Market Arbitrage Bot
    
    This bot crawls multiple prediction market sites, extracts pricing data,
    identifies arbitrage opportunities, and sends notifications.
    """
    
    def __init__(self):
        self.opportunities_found = 0
        self.alerts_sent = 0
        
        # Configuration for different prediction market sites
        self.market_configs = {
            "predictit": {
                "url": "https://www.predictit.org/markets",
                "schema": {
                    "name": "PredictItMarkets",
                    "baseSelector": ".market-card",
                    "fields": [
                        {"name": "event_title", "selector": ".market-title", "type": "text"},
                        {"name": "outcome_name", "selector": ".outcome-name", "type": "text"},
                        {"name": "yes_price", "selector": ".yes-price", "type": "text"},
                        {"name": "no_price", "selector": ".no-price", "type": "text"}
                    ]
                }
            },
            "polymarket": {
                "url": "https://polymarket.com/",
                "schema": {
                    "name": "PolymarketEvents", 
                    "baseSelector": ".event-container",
                    "fields": [
                        {"name": "event_title", "selector": "h3.event-name", "type": "text"},
                        {"name": "outcome_name", "selector": ".outcome-title", "type": "text"},
                        {"name": "price_odds", "selector": ".price-display", "type": "text"}
                    ]
                }
            },
            "kalshi": {
                "url": "https://kalshi.com/markets",
                "schema": {
                    "name": "KalshiMarkets",
                    "baseSelector": ".market-row", 
                    "fields": [
                        {"name": "event_title", "selector": ".market-question", "type": "text"},
                        {"name": "outcome_name", "selector": ".outcome-label", "type": "text"},
                        {"name": "price_cents", "selector": ".price-value", "type": "text"}
                    ]
                }
            }
        }
    
    def normalize_event_title(self, title: str) -> str:
        """Normalize event titles for matching across platforms"""
        normalized = title.lower()
        normalized = normalized.replace("?", "").replace("!", "").replace(".", "")
        normalized = " ".join(normalized.split())
        
        replacements = {
            "bitcoin": "btc",
            "artificial intelligence": "ai",
            "spacex": "spacex",
            "will btc": "btc",
            "btc to": "btc", 
            "by end of": "by",
            "by dec 31": "by",
            "december 31": "dec 31"
        }
        
        for old, new in replacements.items():
            normalized = normalized.replace(old, new)
        
        return normalized
    
    def detect_arbitrage(self, market_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect arbitrage opportunities in market data"""
        print("🔍 Analyzing market data for arbitrage opportunities...")
        
        # Group by normalized event title and outcome
        grouped_events = {}
        for data in market_data:
            normalized_title = self.normalize_event_title(data["event_title"])
            key = f"{normalized_title}_{data['outcome']}"
            
            if key not in grouped_events:
                grouped_events[key] = []
            grouped_events[key].append(data)
        
        opportunities = []
        
        # Check for direct price arbitrage (same outcome, different prices)
        for event_key, event_data in grouped_events.items():
            if len(event_data) < 2:
                continue
                
            prices = [data["price"] for data in event_data]
            sources = [data["source"] for data in event_data]
            
            min_price = min(prices)
            max_price = max(prices)
            
            if max_price > min_price:
                profit_per_share = max_price - min_price
                profit_percentage = (profit_per_share / min_price) * 100
                
                opportunity = {
                    "type": "direct_price_arbitrage",
                    "event_title": event_data[0]["event_title"],
                    "outcome": event_data[0]["outcome"],
                    "sources": sources,
                    "prices": prices,
                    "min_price": min_price,
                    "max_price": max_price,
                    "profit_per_share": profit_per_share,
                    "profit_percentage": profit_percentage,
                    "strategy": f"Buy at ${min_price:.2f}, sell at ${max_price:.2f}",
                    "detected_at": datetime.now().isoformat()
                }
                opportunities.append(opportunity)
        
        # Check for complementary arbitrage (Yes + No < $1)
        events_by_title = {}
        for data in market_data:
            normalized_title = self.normalize_event_title(data["event_title"])
            if normalized_title not in events_by_title:
                events_by_title[normalized_title] = {}
            events_by_title[normalized_title][data["outcome"]] = data
        
        for title, outcomes in events_by_title.items():
            if "Yes" in outcomes and "No" in outcomes:
                yes_price = outcomes["Yes"]["price"]
                no_price = outcomes["No"]["price"]
                total_price = yes_price + no_price
                
                if total_price < 1.0:
                    profit = 1.0 - total_price
                    profit_percentage = (profit / total_price) * 100
                    
                    opportunity = {
                        "type": "complementary_arbitrage",
                        "event_title": outcomes["Yes"]["event_title"],
                        "outcome": "Both (Yes+No)",
                        "sources": [outcomes["Yes"]["source"], outcomes["No"]["source"]],
                        "yes_price": yes_price,
                        "no_price": no_price,
                        "total_cost": total_price,
                        "guaranteed_profit": profit,
                        "profit_percentage": profit_percentage,
                        "strategy": f"Buy Yes at ${yes_price:.2f} + No at ${no_price:.2f} = ${total_price:.2f} < $1.00",
                        "detected_at": datetime.now().isoformat()
                    }
                    opportunities.append(opportunity)
        
        return opportunities
    
    async def crawl_prediction_markets(self, use_mock_data: bool = True) -> List[Dict[str, Any]]:
        """Crawl prediction market sites for current pricing data"""
        if use_mock_data:
            # Return realistic mock data for testing
            return [
                {"source": "PredictIt", "event_title": "Bitcoin to reach $150k in 2025", "outcome": "Yes", "price": 0.35, "timestamp": datetime.now().isoformat()},
                {"source": "Polymarket", "event_title": "Bitcoin to reach $150k in 2025", "outcome": "Yes", "price": 0.28, "timestamp": datetime.now().isoformat()},
                {"source": "Kalshi", "event_title": "AI breakthrough in 2025", "outcome": "Yes", "price": 0.40, "timestamp": datetime.now().isoformat()},
                {"source": "PredictIt", "event_title": "AI breakthrough in 2025", "outcome": "No", "price": 0.55, "timestamp": datetime.now().isoformat()},
            ]
        
        # Real crawling implementation
        print("🌐 Crawling prediction market sites...")
        
        all_market_data = []
        
        async with AsyncWebCrawler() as crawler:
            for market_name, config in self.market_configs.items():
                try:
                    print(f"   📊 Crawling {market_name}...")
                    
                    extraction_strategy = JsonCssExtractionStrategy(schema=config["schema"])
                    crawler_config = CrawlerRunConfig(extraction_strategy=extraction_strategy)
                    
                    result = await crawler.arun(url=config["url"], config=crawler_config)
                    
                    if result.success and result.extracted_content:
                        data = json.loads(result.extracted_content)
                        
                        # Transform data to standard format
                        for item in data:
                            standardized_item = {
                                "source": market_name.title(),
                                "event_title": item.get("event_title", ""),
                                "outcome": item.get("outcome_name", "Yes"),
                                "price": self._parse_price(item),
                                "timestamp": datetime.now().isoformat(),
                                "raw_data": item
                            }
                            all_market_data.append(standardized_item)
                        
                        print(f"   ✅ {market_name}: {len(data)} items extracted")
                    else:
                        print(f"   ❌ {market_name}: Failed to extract data")
                        
                except Exception as e:
                    print(f"   ❌ {market_name}: Error - {e}")
        
        return all_market_data
    
    def _parse_price(self, item: Dict[str, Any]) -> float:
        """Parse price from extracted data (handle different formats)"""
        # Try different price fields that might exist
        price_fields = ["yes_price", "no_price", "price_odds", "price_cents", "price"]
        
        for field in price_fields:
            if field in item and item[field]:
                try:
                    price_str = str(item[field]).replace("$", "").replace("¢", "").replace("%", "")
                    price = float(price_str)
                    
                    # Convert cents to dollars if needed
                    if field == "price_cents" and price > 1:
                        price = price / 100
                    
                    return max(0.01, min(0.99, price))
                except:
                    continue
        
        return 0.5  # Default fallback price
    
    def send_notification(self, opportunity: Dict[str, Any]):
        """Send notification about arbitrage opportunity"""
        message = f"""
🚨 ARBITRAGE OPPORTUNITY DETECTED! 🚨

Event: {opportunity['event_title']}
Type: {opportunity['type'].replace('_', ' ').title()}
Outcome: {opportunity['outcome']}
Sources: {', '.join(opportunity.get('sources', []))}
Strategy: {opportunity['strategy']}
Profit Potential: {opportunity['profit_percentage']:.2f}%
Detected: {opportunity['detected_at']}

Take action quickly - arbitrage opportunities disappear fast!
        """.strip()
        
        print("\n" + "="*60)
        print(message)
        print("="*60)
        
        # Save to alerts log
        with open("arbitrage_alerts.log", "a") as f:
            f.write(f"[{datetime.now().isoformat()}] {message}\n\n")
        
        self.alerts_sent += 1
    
    def save_data(self, market_data: List[Dict[str, Any]], opportunities: List[Dict[str, Any]]):
        """Save market data and opportunities to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save market data
        market_file = f"market_data_{timestamp}.json"
        with open(market_file, "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "total_entries": len(market_data),
                "data": market_data
            }, f, indent=2)
        
        # Save opportunities
        if opportunities:
            opp_file = f"arbitrage_opportunities_{timestamp}.json"
            with open(opp_file, "w") as f:
                json.dump({
                    "timestamp": datetime.now().isoformat(),
                    "total_opportunities": len(opportunities),
                    "opportunities": opportunities
                }, f, indent=2)
            
            print(f"💾 Saved {len(opportunities)} opportunities to {opp_file}")
        
        print(f"💾 Saved {len(market_data)} market entries to {market_file}")
    
    async def run_monitoring_cycle(self, use_mock_data: bool = True):
        """Run a single monitoring cycle"""
        print(f"🔄 Running monitoring cycle at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Step 1: Crawl market data
        market_data = await self.crawl_prediction_markets(use_mock_data=use_mock_data)
        print(f"📊 Collected data from {len(set(d['source'] for d in market_data))} sources")
        
        # Step 2: Detect arbitrage opportunities
        opportunities = self.detect_arbitrage(market_data)
        print(f"🎯 Found {len(opportunities)} arbitrage opportunities")
        
        # Step 3: Send notifications for each opportunity
        for opportunity in opportunities:
            self.send_notification(opportunity)
            self.opportunities_found += 1
        
        # Step 4: Save data
        self.save_data(market_data, opportunities)
        
        return len(opportunities)
    
    async def start_monitoring(self, max_cycles: int = 10, sleep_interval: int = 60, use_mock_data: bool = True):
        """Start continuous monitoring for arbitrage opportunities"""
        print("🤖 Starting Prediction Market Arbitrage Bot")
        print(f"   📊 Max monitoring cycles: {max_cycles}")
        print(f"   ⏰ Sleep interval: {sleep_interval} seconds")
        print(f"   🌐 Using mock data: {use_mock_data}")
        print()
        
        for cycle in range(max_cycles):
            try:
                opportunities_count = await self.run_monitoring_cycle(use_mock_data=use_mock_data)
                
                if cycle < max_cycles - 1:
                    print(f"😴 Sleeping for {sleep_interval} seconds...\n")
                    await asyncio.sleep(sleep_interval)
                    
            except Exception as e:
                print(f"❌ Error in monitoring cycle {cycle + 1}: {e}")
                continue
        
        print(f"\n🎯 Monitoring complete!")
        print(f"   🚨 Total opportunities found: {self.opportunities_found}")
        print(f"   📨 Total alerts sent: {self.alerts_sent}")

async def main():
    """Main function to run the complete arbitrage bot"""
    print("=== Prediction Market Arbitrage Bot ===")
    print("Powered by Crawl4AI - The #1 Trending GitHub Web Crawler\n")
    
    bot = PredictionMarketArbitrageBot()
    
    # Run a few monitoring cycles for demonstration
    await bot.start_monitoring(
        max_cycles=3,
        sleep_interval=10,  # Short interval for demo
        use_mock_data=True  # Set to False for real crawling
    )
    
    print("\n✅ Demo complete!")
    print("\n🚀 Ready for Production:")
    print("  1. Set use_mock_data=False to crawl real sites")
    print("  2. Update market_configs with correct CSS selectors")
    print("  3. Add Slack/Discord webhook notifications")
    print("  4. Connect to Supabase for data persistence")
    print("  5. Deploy to a server or cloud platform")

if __name__ == "__main__":
    asyncio.run(main())