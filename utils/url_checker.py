import requests
from urllib.parse import urljoin

class URLChecker:
    @staticmethod
    def check_url_status(base_url, url):
        try:
            full_url = urljoin(base_url, url)
            response = requests.head(full_url, allow_redirects=True)
            return response.status_code
        except requests.RequestException:
            return 404