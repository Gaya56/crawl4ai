"""
Platform Adapters Package for Multi-Platform Prediction Market Crawling
Following official Crawl4AI modular design patterns

This package provides platform-specific adapters for different prediction market platforms,
enabling clean separation of crawling logic while maintaining compatibility with the
multi-config URL matching system from Step 1.

Reference: /workspaces/crawl4ai/docs/examples/extraction_strategies_examples.py
Official Pattern: Modular strategy design with proper encapsulation

Usage:
    from arbitrage_bot.phase4_multiplatform.platform_adapters import PredictItAdapter, BasePlatformAdapter
    
    adapter = PredictItAdapter()
    config = adapter.create_crawler_config()
"""

from .base_adapter import BasePlatformAdapter
from .predictit_adapter import PredictItAdapter

# Export all adapters for easy importing
__all__ = [
    "BasePlatformAdapter",
    "PredictItAdapter"
]

# Version info for adapter system
__version__ = "1.0.0"
__adapter_version__ = "Phase4_Step2"