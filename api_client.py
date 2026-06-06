"""
Simple and practical API client with error handling and retries
"""

import requests
import time
import json
from typing import Dict, Any, Optional, Union
from logger import get_logger

class APIClient:
    """
    Simple API client with automatic retries and error handling
    
    Usage:
        client = APIClient('https://api.example.com', token='your-token')
        
        # GET request
        response = client.get('/users')
        
        # POST request with JSON data
        response = client.post('/users', json={'name': 'Alice'})
        
        # PUT request
        response = client.put('/users/1', json={'name': 'Bob'})
        
        # DELETE request
        response = client.delete('/users/1')
    """
    
    def __init__(
        self,
        base_url: str,
        token: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: int = 1
    ):
        """
        Initialize API client
        
        Args:
            base_url: Base URL of the API
            token: Bearer token for authentication
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries
            retry_delay: Delay between retries in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.logger = get_logger('api_client')
        
        # Create session
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        # Add authorization header if token provided
        if token:
            self.session.headers.update({
                'Authorization': f'Bearer {token}'
            })
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Union[Dict, str]] = None,
        json_data: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request with retries
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint (e.g., '/users')
            params: Query parameters
            data: Request body (string or dict)
            json_data: JSON request body
            headers: Additional headers
        
        Returns:
            Response as dictionary
        
        Raises:
            Exception: If request fails after all retries
        """
        url = f'{self.base_url}/{endpoint.lstrip("/")}'
        request_headers = self.session.headers.copy()
        
        if headers:
            request_headers.update(headers)
        
        for attempt in range(self.max_retries):
            try:
                self.logger.debug(f'{method} {url} (attempt {attempt + 1}/{self.max_retries})')
                
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    data=data,
                    json=json_data,
                    headers=request_headers,
                    timeout=self.timeout
                )
                
                # Log response
                self.logger.debug(f'Response: {response.status_code}')
                
                # Check for HTTP errors
                response.raise_for_status()
                
                # Try to parse JSON response
                try:
                    return response.json()
                except ValueError:
                    # Return text if not JSON
                    return {'text': response.text, 'status_code': response.status_code}
            
            except requests.exceptions.RequestException as e:
                self.logger.warning(f'Request failed: {e}')
                
                # If last attempt, raise exception
                if attempt == self.max_retries - 1:
                    self.logger.error(f'Request failed after {self.max_retries} attempts')
                    raise Exception(f'API request failed: {e}')
                
                # Wait before retrying
                time.sleep(self.retry_delay * (attempt + 1))
        
        return {}
    
    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        """
        GET request
        
        Args:
            endpoint: API endpoint
            params: Query parameters
        
        Returns:
            Response as dictionary
        """
        return self._request('GET', endpoint, params=params, **kwargs)
    
    def post(self, endpoint: str, json_data: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        """
        POST request
        
        Args:
            endpoint: API endpoint
            json_data: JSON data to send
        
        Returns:
            Response as dictionary
        """
        return self._request('POST', endpoint, json_data=json_data, **kwargs)
    
    def put(self, endpoint: str, json_data: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        """
        PUT request
        
        Args:
            endpoint: API endpoint
            json_data: JSON data to send
        
        Returns:
            Response as dictionary
        """
        return self._request('PUT', endpoint, json_data=json_data, **kwargs)
    
    def patch(self, endpoint: str, json_data: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        """
        PATCH request
        
        Args:
            endpoint: API endpoint
            json_data: JSON data to send
        
        Returns:
            Response as dictionary
        """
        return self._request('PATCH', endpoint, json_data=json_data, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        DELETE request
        
        Args:
            endpoint: API endpoint
        
        Returns:
            Response as dictionary
        """
        return self._request('DELETE', endpoint, **kwargs)
    
    def close(self):
        """Close the session"""
        self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# Example usage
if __name__ == '__main__':
    # Example: Call a public API (JSONPlaceholder)
    print('=== API Client Example ===\n')
    
    # Create client
    client = APIClient('https://jsonplaceholder.typicode.com')
    
    try:
        # GET example
        print('1. GET /posts/1')
        post = client.get('/posts/1')
        print(f'   Title: {post.get("title", "N/A")[:50]}...\n')
        
        # POST example
        print('2. POST /posts (create new)')
        new_post = client.post('/posts', json_data={
            'title': 'Foo',
            'body': 'Bar',
            'userId': 1
        })
        print(f'   Created post ID: {new_post.get("id")}\n')
        
        # PUT example
        print('3. PUT /posts/1 (update)')
        updated = client.put('/posts/1', json_data={
            'id': 1,
            'title': 'Updated Title',
            'body': 'Updated Body',
            'userId': 1
        })
        print(f'   Updated post ID: {updated.get("id")}\n')
        
        # DELETE example
        print('4. DELETE /posts/1')
        result = client.delete('/posts/1')
        print(f'   Delete response: {result}\n')
        
        print('✓ All API calls completed successfully!')
    
    except Exception as e:
        print(f'Error: {e}')
    
    finally:
        client.close()
