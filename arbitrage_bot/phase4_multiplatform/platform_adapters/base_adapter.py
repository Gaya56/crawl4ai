"""
Base Platform Adapter for Multi-Platform Prediction Market Crawling
Following official Crawl4AI extraction strategy patterns from extraction_strategies_examples.py

This module provides the base interface for platform-specific adapters, enabling modular
design and easy integration with the multi-config URL matching system from Step 1.

Reference: /workspaces/crawl4ai/docs/examples/extraction_strategies_examples.py
Official Pattern: Modular strategy design with proper encapsulation
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from crawl4ai import CrawlerRunConfig
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy


class BasePlatformAdapter(ABC):
    """
    Abstract base class for prediction market platform adapters.
    
    Following the official Crawl4AI pattern from extraction_strategies_examples.py
    where each strategy is self-contained and provides its own configuration.
    
    Each platform adapter encapsulates:
    - URL matching patterns
    - CSS extraction schemas  
    - JavaScript execution code
    - Wait conditions for dynamic content
    - Platform-specific error handling
    
    Reference: /workspaces/crawl4ai/docs/examples/extraction_strategies_examples.py:lines 25-45
    """
    
    def __init__(self, platform_name: str):
        """Initialize the adapter with platform identification."""
        self.platform_name = platform_name
        self._schema_cache: Optional[Dict[str, Any]] = None
        self._config_cache: Optional[CrawlerRunConfig] = None
    
    @property
    @abstractmethod
    def url_patterns(self) -> List[str]:
        """
        Return URL patterns that this adapter handles.
        Used for URL matching in multi-config approach.
        
        Example: ["*predictit.org*", "*predictit.com*"]
        """
        pass
    
    @property
    @abstractmethod
    def base_urls(self) -> List[str]:
        """
        Return base URLs for this platform for testing/monitoring.
        
        Example: ["https://www.predictit.org/markets/21/Elections"]
        """
        pass
    
    @abstractmethod
    def get_extraction_schema(self) -> Dict[str, Any]:
        """
        Return platform-specific CSS extraction schema.
        
        Following JsonCssExtractionStrategy pattern from official examples.
        Schema format matches extraction_strategies_examples.py CSS schema structure.
        
        Returns:
            Dict containing baseSelector and fields for CSS extraction
        """
        pass
    
    @abstractmethod
    def get_javascript_code(self) -> List[str]:
        """
        Return platform-specific JavaScript code for dynamic content handling.
        
        Following the official pattern from demo_multi_config_clean.py for js_code.
        Should return list of JavaScript strings to execute.
        
        Returns:
            List of JavaScript code strings
        """
        pass
    
    @abstractmethod
    def get_wait_conditions(self) -> Optional[str]:
        """
        Return CSS selectors to wait for before extraction.
        
        Following CrawlerRunConfig wait_for pattern from official examples.
        
        Returns:
            CSS selector string or None if no waiting required
        """
        pass
    
    def create_extraction_strategy(self) -> JsonCssExtractionStrategy:
        """
        Create JsonCssExtractionStrategy instance for this platform.
        
        Following official pattern from extraction_strategies_examples.py:lines 95-100
        where CSS extraction strategy is created with platform-specific schema.
        
        Returns:
            Configured JsonCssExtractionStrategy instance
        """
        if self._schema_cache is None:
            self._schema_cache = self.get_extraction_schema()
        
        return JsonCssExtractionStrategy(schema=self._schema_cache)
    
    def create_crawler_config(self) -> CrawlerRunConfig:
        """
        Create CrawlerRunConfig for this platform following multi-config pattern.
        
        Combines all platform-specific settings into a single configuration object
        compatible with the multi-config URL matching approach from Step 1.
        
        Reference: 
        - /workspaces/crawl4ai/docs/examples/demo_multi_config_clean.py:lines 124-160
        - Step 1 implementation in multi_platform_crawler.py
        
        Returns:
            Configured CrawlerRunConfig instance
        """
        if self._config_cache is None:
            # Get platform-specific components
            extraction_strategy = self.create_extraction_strategy()
            js_code = self.get_javascript_code()
            wait_conditions = self.get_wait_conditions()
            url_pattern = self.url_patterns[0]  # Use primary URL pattern
            
            # Create config following official multi-config pattern
            config_params = {
                "url_matcher": url_pattern,
                "extraction_strategy": extraction_strategy
            }
            
            # Add JavaScript code if provided
            if js_code:
                config_params["js_code"] = js_code
            
            # Add wait conditions if provided  
            if wait_conditions:
                config_params["wait_for"] = wait_conditions
            
            self._config_cache = CrawlerRunConfig(**config_params)
        
        return self._config_cache
    
    async def run_extraction(self, crawler, url: str) -> Dict[str, Any]:
        """
        Run extraction for a specific URL using this adapter.
        
        Following the helper function pattern from extraction_strategies_examples.py:lines 25-45
        for encapsulated extraction with proper error handling.
        
        Args:
            crawler: AsyncWebCrawler instance
            url: URL to crawl
            
        Returns:
            Dict containing extraction results and metadata
        """
        try:
            config = self.create_crawler_config()
            result = await crawler.arun(url=url, config=config)
            
            return {
                "success": result.success,
                "platform": self.platform_name,
                "url": url,
                "title": result.metadata.get("title", "N/A"),
                "content_size": len(result.markdown),
                "extracted_content": result.extracted_content,
                "error_message": result.error_message if not result.success else None
            }
            
        except Exception as e:
            return {
                "success": False,
                "platform": self.platform_name,
                "url": url,
                "error_message": f"Adapter error: {str(e)}"
            }
    
    def get_platform_info(self) -> Dict[str, Any]:
        """
        Return platform information for debugging and monitoring.
        
        Returns:
            Dict containing platform metadata
        """
        return {
            "platform_name": self.platform_name,
            "url_patterns": self.url_patterns,
            "base_urls": self.base_urls,
            "has_extraction_schema": bool(self.get_extraction_schema()),
            "has_javascript": bool(self.get_javascript_code()),
            "has_wait_conditions": bool(self.get_wait_conditions())
        }