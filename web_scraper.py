"""
Simple web scraper with requests and BeautifulSoup
Requires: requests, beautifulsoup4
"""

import requests
from typing import Dict, List, Optional, Any
from logger import get_logger

logger = get_logger('web_scraper')


class WebScraper:
    """
    Simple web scraper for common tasks
    
    Usage:
        scraper = WebScraper()
        
        # GET request
        response = scraper.get('https://example.com')
        
        # Parse HTML
        if response:
            title = scraper.get_title(response.text)
            links = scraper.get_links(response.text)
            text = scraper.get_text(response.text)
        
        # POST request
        response = scraper.post('https://api.example.com', json_data={'key': 'value'})
        
        # Download file
        scraper.download_file('https://example.com/file.pdf', 'output/file.pdf')
    """
    
    def __init__(self, timeout: int = 30, max_retries: int = 3):
        """
        Initialize web scraper
        
        Args:
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        logger.info(f'WebScraper initialized (timeout={timeout}s, retries={max_retries})')
    
    def get(self, url: str, params: Optional[Dict] = None) -> Optional[requests.Response]:
        """
        GET request
        
        Args:
            url: URL to fetch
            params: Query parameters
        
        Returns:
            Response object or None
        """
        try:
            logger.debug(f'GET {url}')
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            logger.info(f'GET {url} - {response.status_code}')
            return response
        except Exception as e:
            logger.error(f'GET {url} failed: {e}')
            return None
    
    def post(self, url: str, json_data: Optional[Dict] = None, data: Optional[Dict] = None) -> Optional[requests.Response]:
        """
        POST request
        
        Args:
            url: URL to post to
            json_data: JSON data to send
            data: Form data to send
        
        Returns:
            Response object or None
        """
        try:
            logger.debug(f'POST {url}')
            response = self.session.post(url, json=json_data, data=data, timeout=self.timeout)
            response.raise_for_status()
            logger.info(f'POST {url} - {response.status_code}')
            return response
        except Exception as e:
            logger.error(f'POST {url} failed: {e}')
            return None
    
    def download_file(self, url: str, filepath: str) -> bool:
        """
        Download file from URL
        
        Args:
            url: URL of file to download
            filepath: Local path to save file
        
        Returns:
            True if successful
        """
        try:
            import os
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            logger.debug(f'Downloading {url} to {filepath}')
            response = self.session.get(url, timeout=self.timeout, stream=True)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            logger.info(f'Downloaded {url} -> {filepath}')
            return True
        except Exception as e:
            logger.error(f'Download failed {url}: {e}')
            return False
    
    def get_title(self, html: str) -> Optional[str]:
        """
        Extract title from HTML
        
        Args:
            html: HTML content
        
        Returns:
            Title text or None
        """
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.find('title')
            return title.text.strip() if title else None
        except ImportError:
            logger.error('beautifulsoup4 not installed. Run: pip install beautifulsoup4')
            return None
        except Exception as e:
            logger.error(f'Error extracting title: {e}')
            return None
    
    def get_links(self, html: str, base_url: str = '') -> List[str]:
        """
        Extract all links from HTML
        
        Args:
            html: HTML content
            base_url: Base URL to prepend to relative links
        
        Returns:
            List of links
        """
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if base_url and not href.startswith(('http://', 'https://')):
                    href = base_url.rstrip('/') + '/' + href.lstrip('/')
                links.append(href)
            logger.debug(f'Extracted {len(links)} links')
            return links
        except ImportError:
            logger.error('beautifulsoup4 not installed. Run: pip install beautifulsoup4')
            return []
        except Exception as e:
            logger.error(f'Error extracting links: {e}')
            return []
    
    def get_text(self, html: str) -> str:
        """
        Extract readable text from HTML
        
        Args:
            html: HTML content
        
        Returns:
            Extracted text
        """
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            # Remove script and style elements
            for script in soup(['script', 'style']):
                script.decompose()
            text = soup.get_text()
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split('  '))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            return text
        except ImportError:
            logger.error('beautifulsoup4 not installed. Run: pip install beautifulsoup4')
            return ''
        except Exception as e:
            logger.error(f'Error extracting text: {e}')
            return ''
    
    def search_in_html(self, html: str, selector: str) -> List[Any]:
        """
        Search HTML using CSS selector
        
        Args:
            html: HTML content
            selector: CSS selector
        
        Returns:
            List of matching elements
        """
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            elements = soup.select(selector)
            logger.debug(f'Found {len(elements)} elements matching "{selector}"')
            return elements
        except ImportError:
            logger.error('beautifulsoup4 not installed. Run: pip install beautifulsoup4')
            return []
        except Exception as e:
            logger.error(f'Error searching HTML: {e}')
            return []
    
    def close(self):
        """Close session"""
        self.session.close()
        logger.info('WebScraper session closed')
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# Example usage
if __name__ == '__main__':
    print('=== WebScraper Example ===\n')
    
    # Create scraper
    scraper = WebScraper()
    
    try:
        # Example 1: GET request
        print('1. Fetching example.com...')
        response = scraper.get('https://example.com')
        if response:
            print(f'   Status: {response.status_code}')
            print(f'   Content-Type: {response.headers.get("content-type")}')
            
            # Extract title (requires beautifulsoup4)
            # title = scraper.get_title(response.text)
            # print(f'   Title: {title}')
        
        # Example 2: Download file
        print('\n2. Downloading robots.txt...')
        success = scraper.download_file('https://example.com/robots.txt', 'output/robots.txt')
        if success:
            print('   Downloaded to output/robots.txt')
        
        # Example 3: API call
        print('\n3. Calling JSONPlaceholder API...')
        response = scraper.get('https://jsonplaceholder.typicode.com/posts/1')
        if response:
            data = response.json()
            print(f'   Title: {data.get("title", "")[:50]}...')
        
        print('\n[OK] WebScraper examples completed!')
        print('   (Install beautifulsoup4 for HTML parsing: pip install beautifulsoup4)')
        
    except Exception as e:
        print(f'Error: {e}')
    finally:
        scraper.close()
