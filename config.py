"""Configuration module for the research assistant."""
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class Config:
    """Configuration class for the research assistant."""
    
    # Google Gemini API
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GEMINI_MODEL: str = "gemini-pro"
    TEMPERATURE: float = 0.7
    
    # Chroma settings
    CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", ".chroma")
    COLLECTION_NAME: str = "research_memory"
    
    # Web scraping settings
    REQUEST_TIMEOUT: int = 30
    MAX_RETRIES: int = 3
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    # Output settings
    REPORTS_DIR: str = os.getenv("REPORTS_DIR", "reports")
    VISUALIZATIONS_DIR: str = os.getenv("VISUALIZATIONS_DIR", "visualizations")
    
    # Agent settings
    MAX_ITERATIONS: int = 5
    CONFIDENCE_THRESHOLD: float = 0.7
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in .env file.")
        return True

