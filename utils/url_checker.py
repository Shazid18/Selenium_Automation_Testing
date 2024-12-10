import requests
from urllib.parse import urljoin
from config.config import REQUEST_TIMEOUT

class URLChecker:
    @staticmethod
    def check_url_status(base_url, url):
        """
        Checks the status of a URL by combining it with the base URL.
        
        Args:
            base_url (str): The base URL to resolve relative URLs.
            url (str): The relative or absolute URL to check.
            timeout (int, optional): Timeout in seconds for the request. Default is 5 seconds.

        Returns:
            tuple: A tuple containing the status code and the final resolved URL.
        """
        try:
            # Combine the base URL with the relative URL
            full_url = urljoin(base_url, url)
            # Send a HEAD request to the URL with a timeout
            response = requests.head(full_url, allow_redirects=True, timeout=REQUEST_TIMEOUT)
            
            # Return the status code and the final resolved URL
            return response.status_code, response.url
        
        except requests.RequestException as e:
            # Return 404 if there is a request exception and log the error
            print(f"Error checking URL {url}: {e}")
            return 404, url  # Returning the original URL for transparency

