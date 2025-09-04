"""
Phase 3: Real Arbitrage Detection with Extracted Market Data
Processing actual PredictIt data to find arbitrage opportunities
"""
import asyncio
import json
import re
from typing import List, Dict, Optional
from dataclasses import dataclass
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai import JsonCssExtractionStrategy


@dataclass
class MarketData:
    event_title: str
    candidate: str
    price_cents: int
    platform: str
    market_url: str
    volume: Optional[str] = None


@dataclass 
class ArbitrageOpportunity:
    event: str
    candidate: str
    platform_a: str
    price_a: int
    platform_b: str
    price_b: int
    profit_margin: float
    details: Dict


def parse_price(price_text: str) -> Optional[int]:
    """Extract price in cents from text like '34¢' or '$0.34'"""
    if not price_text:
        return None
    
    # Look for cents pattern like '34¢'
    cents_match = re.search(r'(\d+)¢', price_text)
    if cents_match:
        return int(cents_match.group(1))
    
    # Look for dollar pattern like '$0.34'
    dollar_match = re.search(r'\$0\.(\d+)', price_text)
    if dollar_match:
        return int(dollar_match.group(1))
    
    # Look for plain numbers
    number_match = re.search(r'(\d+)', price_text)
    if number_match:
        return int(number_match.group(1))
    
    return None


def extract_candidate_from_text(text: str) -> str:
    """Extract candidate name from mixed text"""
    # Common patterns in PredictIt data
    if 'Gavin Newsom' in text:
        return 'Gavin Newsom'
    elif 'A. Ocasio-Cortez' in text:
        return 'Alexandria Ocasio-Cortez'
    elif 'Democratic presidential nominee' in text:
        return 'Democratic Nominee'
    
    # Extract first reasonable candidate name
    words = text.split()
    for i, word in enumerate(words):
        if word[0].isupper() and i + 1 < len(words) and words[i+1][0].isupper():
            return f"{word} {words[i+1]}"
    
    return text[:50]  # Fallback


def process_predictit_data(extracted_items: List[Dict]) -> List[MarketData]:
    """Convert raw PredictIt extraction into structured MarketData objects"""
    market_data = []
    
    for item in extracted_items:
        title = item.get('title', '')
        price_text = item.get('all_prices', '') or item.get('no_price', '')
        link = item.get('links', '')
        
        if title and price_text:
            price_cents = parse_price(price_text)
            if price_cents is not None:
                candidate = extract_candidate_from_text(price_text + ' ' + title)
                
                market_data.append(MarketData(
                    event_title=title,
                    candidate=candidate,
                    price_cents=price_cents,
                    platform='PredictIt',
                    market_url=f"https://www.predictit.org{link}" if link.startswith('/') else link,
                    volume=extract_volume(price_text)
                ))
    
    return market_data


def extract_volume(text: str) -> Optional[str]:
    """Extract trading volume from text"""
    volume_match = re.search(r'(\d+K?)\s*Shares?\s*Traded', text)
    return volume_match.group(1) if volume_match else None


def detect_arbitrage_opportunities(market_data: List[MarketData]) -> List[ArbitrageOpportunity]:
    """
    Detect arbitrage opportunities in market data
    
    For prediction markets, arbitrage occurs when:
    1. Same event/candidate has different prices on different platforms
    2. Complementary outcomes (Yes/No) don't add up to 100¢ 
    """
    opportunities = []
    
    # Group by event for comparison
    events = {}
    for data in market_data:
        event_key = data.event_title.lower().strip()
        if event_key not in events:
            events[event_key] = []
        events[event_key].append(data)
    
    for event_title, event_data in events.items():
        # Check for complementary arbitrage (Yes + No ≠ 100¢)
        candidates = {}
        for data in event_data:
            candidate_key = data.candidate.lower().strip()
            if candidate_key not in candidates:
                candidates[candidate_key] = []
            candidates[candidate_key].append(data)
        
        # Simple arbitrage check: if multiple prices for same candidate
        for candidate, prices in candidates.items():
            if len(prices) > 1:
                prices.sort(key=lambda x: x.price_cents)
                min_price = prices[0]
                max_price = prices[-1]
                
                if max_price.price_cents > min_price.price_cents:
                    profit_margin = max_price.price_cents - min_price.price_cents
                    
                    opportunities.append(ArbitrageOpportunity(
                        event=event_title,
                        candidate=candidate,
                        platform_a=min_price.platform,
                        price_a=min_price.price_cents,
                        platform_b=max_price.platform, 
                        price_b=max_price.price_cents,
                        profit_margin=profit_margin,
                        details={
                            'url_a': min_price.market_url,
                            'url_b': max_price.market_url,
                            'volume_a': min_price.volume,
                            'volume_b': max_price.volume
                        }
                    ))
    
    return opportunities


async def crawl_and_detect_arbitrage():
    """Main function to crawl markets and detect arbitrage"""
    print("=== Phase 3: Real Arbitrage Detection ===")
    print("Crawling PredictIt markets and analyzing for arbitrage opportunities...")
    
    browser_config = BrowserConfig(headless=True, verbose=True)
    
    # Target multiple PredictIt market categories
    market_urls = [
        "https://www.predictit.org/markets/21/Elections",
        "https://www.predictit.org/markets/3/President", 
        "https://www.predictit.org/markets/2/Congress"
    ]
    
    all_market_data = []
    
    schema = {
        "name": "PredictItMarkets",
        "baseSelector": "div[class*='market'], article, .card, div",
        "fields": [
            {"name": "title", "selector": "h1, h2, h3, .title, [data-test*='title']", "type": "text"},
            {"name": "all_prices", "selector": "[class*='price'], .price", "type": "text"}, 
            {"name": "links", "selector": "a", "type": "attribute", "attribute": "href"},
            {"name": "content", "selector": "*", "type": "text"}
        ]
    }
    
    extraction_strategy = JsonCssExtractionStrategy(schema)
    
    async with AsyncWebCrawler(config=browser_config) as crawler:
        for url in market_urls:
            print(f"\n📡 Crawling: {url}")
            
            config = CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                extraction_strategy=extraction_strategy,
                js_code=[
                    "await new Promise(resolve => setTimeout(resolve, 3000));",
                ]
            )
            
            result = await crawler.arun(url=url, config=config)
            
            if result.success:
                try:
                    extracted_data = json.loads(result.extracted_content)
                    market_data = process_predictit_data(extracted_data)
                    all_market_data.extend(market_data)
                    print(f"✅ Extracted {len(market_data)} market entries")
                    
                except json.JSONDecodeError as e:
                    print(f"❌ JSON parsing error: {e}")
            else:
                print(f"❌ Crawl failed: {result.error_message}")
    
    print(f"\n📊 Total market data collected: {len(all_market_data)}")
    
    # Show sample of collected data
    print("\n🔍 Sample Market Data:")
    for i, data in enumerate(all_market_data[:5]):
        print(f"{i+1}. {data.candidate} - {data.price_cents}¢ ({data.platform})")
    
    # Detect arbitrage opportunities
    print("\n🎯 Detecting Arbitrage Opportunities...")
    opportunities = detect_arbitrage_opportunities(all_market_data)
    
    if opportunities:
        print(f"🚨 Found {len(opportunities)} arbitrage opportunities!")
        for i, opp in enumerate(opportunities):
            print(f"\n💰 Opportunity #{i+1}:")
            print(f"   Event: {opp.event}")
            print(f"   Candidate: {opp.candidate}")
            print(f"   Buy at {opp.platform_a}: {opp.price_a}¢")
            print(f"   Sell at {opp.platform_b}: {opp.price_b}¢")
            print(f"   Profit Margin: {opp.profit_margin}¢")
    else:
        print("💡 No arbitrage opportunities found in current data")
        print("   (This is normal - arbitrage opportunities are rare)")
    
    # Save data for analysis
    output_file = "real_market_data.json"
    with open(output_file, 'w') as f:
        json.dump([
            {
                'event': data.event_title,
                'candidate': data.candidate, 
                'price_cents': data.price_cents,
                'platform': data.platform,
                'url': data.market_url,
                'volume': data.volume
            } for data in all_market_data
        ], f, indent=2)
    
    print(f"\n💾 Saved market data to: {output_file}")
    return all_market_data, opportunities


if __name__ == "__main__":
    asyncio.run(crawl_and_detect_arbitrage())