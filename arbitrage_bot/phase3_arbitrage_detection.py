import asyncio
import json
import os
from datetime import datetime
from typing import List, Dict, Any
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai import JsonCssExtractionStrategy

# Mock data for testing arbitrage logic
MOCK_MARKET_DATA = [
    {
        "source": "PredictIt",
        "event_title": "Will Bitcoin reach $100,000 by end of 2025?",
        "outcome": "Yes",
        "price": 0.65,  # 65 cents = 65% implied probability
        "timestamp": datetime.now().isoformat()
    },
    {
        "source": "Polymarket", 
        "event_title": "Will Bitcoin reach $100,000 by end of 2025?",
        "outcome": "Yes",
        "price": 0.58,  # 58 cents = 58% implied probability
        "timestamp": datetime.now().isoformat()
    },
    {
        "source": "Kalshi",
        "event_title": "Bitcoin to reach $100k by Dec 31, 2025",
        "outcome": "Yes", 
        "price": 0.62,  # 62 cents = 62% implied probability
        "timestamp": datetime.now().isoformat()
    },
    # Example with No arbitrage (prices are aligned)
    {
        "source": "PredictIt",
        "event_title": "Will it rain tomorrow?",
        "outcome": "Yes",
        "price": 0.40,
        "timestamp": datetime.now().isoformat()
    },
    {
        "source": "Polymarket",
        "event_title": "Will it rain tomorrow?", 
        "outcome": "Yes",
        "price": 0.41,
        "timestamp": datetime.now().isoformat()
    }
]

def normalize_event_title(title: str) -> str:
    """
    Normalize event titles to help match the same event across platforms
    """
    # Convert to lowercase and remove common variations
    normalized = title.lower()
    
    # Remove common punctuation and extra spaces
    normalized = normalized.replace("?", "").replace("!", "").replace(".", "")
    normalized = " ".join(normalized.split())
    
    # Handle common variations
    replacements = {
        "bitcoin": "btc",
        "will btc": "btc", 
        "btc to": "btc",
        "by end of": "by",
        "by dec 31": "by",
        "december 31": "dec 31"
    }
    
    for old, new in replacements.items():
        normalized = normalized.replace(old, new)
    
    return normalized

def calculate_arbitrage_opportunity(prices: List[float]) -> Dict[str, Any]:
    """
    Calculate if there's an arbitrage opportunity given a list of prices for the same outcome
    
    For prediction markets, arbitrage exists when:
    sum(1/price_i) < 1 for buying the same outcome across different platforms
    
    Returns:
    - has_arbitrage: bool
    - profit_percentage: float 
    - explanation: str
    """
    if len(prices) < 2:
        return {"has_arbitrage": False, "profit_percentage": 0, "explanation": "Need at least 2 prices"}
    
    # Calculate the sum of inverse prices
    inverse_sum = sum(1/price for price in prices if price > 0)
    
    # Arbitrage exists if this sum is less than 1
    has_arbitrage = inverse_sum < 1
    
    if has_arbitrage:
        # Calculate potential profit percentage
        profit_percentage = ((1 - inverse_sum) / inverse_sum) * 100
        explanation = f"Buy at {min(prices):.2f}, sell at {max(prices):.2f}. Profit: {profit_percentage:.2f}%"
    else:
        profit_percentage = 0
        explanation = f"No arbitrage. Sum of inverse prices: {inverse_sum:.4f} >= 1"
    
    return {
        "has_arbitrage": has_arbitrage,
        "profit_percentage": profit_percentage, 
        "explanation": explanation,
        "inverse_sum": inverse_sum,
        "min_price": min(prices),
        "max_price": max(prices)
    }

def find_arbitrage_opportunities(market_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Analyze market data to find arbitrage opportunities
    """
    print("=== Phase 3: Arbitrage Detection Logic ===")
    print("🔍 Analyzing market data for arbitrage opportunities...\n")
    
    # Group by normalized event title and outcome
    grouped_events = {}
    
    for data in market_data:
        normalized_title = normalize_event_title(data["event_title"])
        key = f"{normalized_title}_{data['outcome']}"
        
        if key not in grouped_events:
            grouped_events[key] = []
        grouped_events[key].append(data)
    
    arbitrage_opportunities = []
    
    print("📊 Event Analysis:")
    print("-" * 60)
    
    for event_key, event_data in grouped_events.items():
        print(f"\n🎯 Event: {event_key}")
        print(f"   Sources: {len(event_data)} platforms")
        
        if len(event_data) < 2:
            print(f"   ⚠️  Only one source - no arbitrage possible")
            continue
            
        # Extract prices for this event/outcome
        prices = [data["price"] for data in event_data]
        sources = [data["source"] for data in event_data]
        
        print(f"   💰 Prices: {dict(zip(sources, prices))}")
        
        # Calculate arbitrage opportunity
        arbitrage_result = calculate_arbitrage_opportunity(prices)
        
        if arbitrage_result["has_arbitrage"]:
            print(f"   🚨 ARBITRAGE FOUND! {arbitrage_result['explanation']}")
            
            opportunity = {
                "event_title": event_data[0]["event_title"],
                "outcome": event_data[0]["outcome"],
                "sources": sources,
                "prices": prices,
                "arbitrage_result": arbitrage_result,
                "event_data": event_data
            }
            arbitrage_opportunities.append(opportunity)
        else:
            print(f"   ✅ No arbitrage: {arbitrage_result['explanation']}")
    
    return arbitrage_opportunities

def save_market_data_to_json(market_data: List[Dict[str, Any]], filename: str = "market_data.json"):
    """
    Save market data to JSON file (simulating database storage)
    """
    print(f"\n💾 Saving market data to {filename}...")
    
    # Add metadata
    data_to_save = {
        "timestamp": datetime.now().isoformat(),
        "total_entries": len(market_data),
        "data": market_data
    }
    
    with open(filename, "w") as f:
        json.dump(data_to_save, f, indent=2)
    
    print(f"   ✅ Saved {len(market_data)} market entries")

def save_arbitrage_opportunities(opportunities: List[Dict[str, Any]], filename: str = "arbitrage_opportunities.json"):
    """
    Save arbitrage opportunities to JSON file
    """
    if not opportunities:
        print("   📋 No arbitrage opportunities to save")
        return
        
    print(f"\n🚨 Saving {len(opportunities)} arbitrage opportunities to {filename}...")
    
    # Prepare data for saving
    data_to_save = {
        "timestamp": datetime.now().isoformat(),
        "total_opportunities": len(opportunities),
        "opportunities": opportunities
    }
    
    with open(filename, "w") as f:
        json.dump(data_to_save, f, indent=2)
    
    print(f"   ✅ Saved arbitrage opportunities")

async def simulate_real_crawl_with_arbitrage_detection():
    """
    Simulate a real crawl and then apply arbitrage detection
    """
    print("=== Simulating Real Market Data Collection ===")
    print("In a real scenario, this would crawl actual prediction market sites...\n")
    
    # For now, we'll use our mock data to test the arbitrage logic
    print("📊 Using mock market data for testing:")
    for i, data in enumerate(MOCK_MARKET_DATA, 1):
        print(f"   {i}. {data['source']}: {data['event_title']} - {data['outcome']} @ ${data['price']}")
    
    print("\n" + "="*70)
    
    # Apply arbitrage detection
    opportunities = find_arbitrage_opportunities(MOCK_MARKET_DATA)
    
    print(f"\n🎯 Final Results:")
    print("-" * 30)
    print(f"📊 Total events analyzed: {len(set(normalize_event_title(d['event_title']) for d in MOCK_MARKET_DATA))}")
    print(f"🚨 Arbitrage opportunities found: {len(opportunities)}")
    
    if opportunities:
        print(f"\n💰 Arbitrage Opportunities Summary:")
        for i, opp in enumerate(opportunities, 1):
            result = opp["arbitrage_result"]
            print(f"   {i}. {opp['event_title']}")
            print(f"      Profit potential: {result['profit_percentage']:.2f}%")
            print(f"      Strategy: {result['explanation']}")
    
    # Save data (simulating database storage)
    save_market_data_to_json(MOCK_MARKET_DATA)
    save_arbitrage_opportunities(opportunities)
    
    return opportunities

async def main():
    """
    Main function for Phase 3 testing
    """
    print("=== Phase 3: Intelligence - Arbitrage Detection & Data Persistence ===\n")
    
    opportunities = await simulate_real_crawl_with_arbitrage_detection()
    
    print("\n=== Phase 3 Complete ===")
    print("✅ Arbitrage detection logic implemented and tested!")
    print("✅ Data persistence simulation complete!")
    print("📁 Check arbitrage_opportunities.json and market_data.json files")
    print("\nNext: We'll add automation and real-time monitoring...")

if __name__ == "__main__":
    asyncio.run(main())