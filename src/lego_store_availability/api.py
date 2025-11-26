"""
LEGO API
"""

from logging import getLogger
from typing import Generator

from httpx import Client as HttpxClient
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential

from .store import LegoStore

logger = getLogger(__name__)


class LegoAPI:
    """LEGO API"""

    base_url = "https://www.lego.com"

    def __init__(self):
        self.client = HttpxClient(
            base_url=self.base_url,
            headers={"User-Agent": "Lunik/lego-store-availability"},
        )

    def __repr__(self):
        return "<LegoAPI>"

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def get_page(self, path: str = "/") -> BeautifulSoup:
        """Get a page from the LEGO website"""

        response = self.client.get(url=path, follow_redirects=True)
        response.raise_for_status()

        return BeautifulSoup(response.content.decode("UTF-8"), "html.parser")

    def get_list_page(self, path: str = "/") -> Generator[BeautifulSoup, None, None]:
        """Get a list page from the LEGO website"""

        next_path = path

        while next_path:
            soup = self.get_page(path=next_path)
            yield soup

            nav_next = soup.find("a", {"rel": "next"})
            next_path = nav_next.get("href") if nav_next else None

    def store(self, lang: str) -> LegoStore:
        """Get a store by lang"""

        store = LegoStore(
            lego_api=self,
            lang=lang,
        )

        return store
