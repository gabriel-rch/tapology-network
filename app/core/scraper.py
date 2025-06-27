from httpx import Client
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self):
        self.base_url = "https://www.tapology.com"
        self.ua_fabric = UserAgent()
        self.client = Client(headers={"User-Agent": self.ua_fabric.random})

    def shuffle_user_agent(self):
        """
        Shuffle the User-Agent header to avoid detection.
        """
        self.client.headers["User-Agent"] = self.ua_fabric.random

    def get(self, path):
        self.shuffle_user_agent()
        response = self.client.get(self.base_url + path)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    def close(self):
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
