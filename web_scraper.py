"""Web scraping module using Beautiful Soup."""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import time
from urllib.parse import urljoin, urlparse
from config import Config
import re

class WebScraper:
    """Web scraper using Beautiful Soup."""
    
    def __init__(self):
        """Initialize the web scraper."""
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": Config.USER_AGENT
        })
        self.timeout = Config.REQUEST_TIMEOUT
    
    def fetch_page(self, url: str, retries: int = Config.MAX_RETRIES) -> Optional[BeautifulSoup]:
        """Fetch and parse a web page."""
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                return BeautifulSoup(response.content, 'lxml')
            except Exception as e:
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                print(f"Error fetching {url}: {e}")
                return None
        return None
    
    def extract_text(self, soup: BeautifulSoup) -> str:
        """Extract main text content from a page."""
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def extract_links(self, soup: BeautifulSoup, base_url: str, limit: int = 10) -> List[str]:
        """Extract relevant links from a page."""
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            absolute_url = urljoin(base_url, href)
            
            # Filter out non-HTTP links and common non-content URLs
            if urlparse(absolute_url).scheme in ['http', 'https']:
                if not any(excluded in absolute_url.lower() for excluded in 
                          ['javascript:', 'mailto:', '#', 'pdf', 'download']):
                    links.append(absolute_url)
            
            if len(links) >= limit:
                break
        
        return links
    
    def extract_tables(self, soup: BeautifulSoup) -> List[Dict[str, any]]:
        """Extract data tables from a page."""
        tables = []
        for table in soup.find_all('table'):
            rows = []
            headers = []
            
            # Extract headers
            header_row = table.find('tr')
            if header_row:
                headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]
            
            # Extract data rows
            for row in table.find_all('tr')[1:]:  # Skip header row
                cells = [td.get_text(strip=True) for td in row.find_all(['td', 'th'])]
                if cells:
                    rows.append(cells)
            
            if rows:
                tables.append({
                    "headers": headers,
                    "rows": rows
                })
        
        return tables
    
    def extract_article_metadata(self, soup: BeautifulSoup) -> Dict[str, Optional[str]]:
        """Extract article metadata (title, author, date, etc.)."""
        metadata = {}
        
        # Title
        title_tag = soup.find('title')
        if not title_tag:
            title_tag = soup.find('h1')
        metadata['title'] = title_tag.get_text(strip=True) if title_tag else None
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        metadata['description'] = meta_desc.get('content') if meta_desc else None
        
        # Author
        author_tag = soup.find('meta', attrs={'name': 'author'}) or \
                    soup.find('meta', attrs={'property': 'article:author'})
        metadata['author'] = author_tag.get('content') if author_tag else None
        
        # Date
        date_tag = soup.find('meta', attrs={'property': 'article:published_time'}) or \
                  soup.find('time')
        if date_tag:
            metadata['date'] = date_tag.get('content') or date_tag.get('datetime') or \
                             date_tag.get_text(strip=True)
        else:
            metadata['date'] = None
        
        return metadata
    
    def scrape_research_article(self, url: str) -> Dict[str, any]:
        """Scrape a research article and extract all relevant information."""
        soup = self.fetch_page(url)
        if not soup:
            return {"error": f"Failed to fetch {url}"}
        
        return {
            "url": url,
            "metadata": self.extract_article_metadata(soup),
            "text": self.extract_text(soup),
            "tables": self.extract_tables(soup),
            "links": self.extract_links(soup, url),
            "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def search_and_scrape(self, search_query: str, max_results: int = 5) -> List[Dict[str, any]]:
        """Search for articles and scrape them (simplified - in production, use proper search API)."""
        # Note: This is a simplified version. In production, you'd use:
        # - Google Custom Search API
        # - arXiv API
        # - PubMed API
        # - Semantic Scholar API
        # etc.
        
        # For now, return empty list - this would be implemented with actual search APIs
        # The user can extend this with their preferred search method
        results = []
        
        # Example: If you have search URLs, you could scrape them here
        # For demonstration, we'll return an empty list that can be populated
        
        return results

