"""
Lego Store
"""

from typing import Generator
from logging import getLogger

from .product import LegoProduct

logger = getLogger(__name__)


class LegoStore:
    """Lego Store"""

    def __init__(self, lego_api: "LegoAPI", lang: str = "fr-fr"):
        self._lego_api = lego_api
        self.lang = lang

    def __repr__(self):
        return f"<LegoStore {self.lang}>"

    @property
    def base_url(self) -> str:
        """Get the base url"""

        return f"/{self.lang}"

    def get_list_page(self, path: str) -> Generator[LegoProduct, None, None]:
        """Get a list page"""

        for soup in self._lego_api.get_list_page(
            path=path,
        ):
            for article in soup.find_all("article", {"data-test": "product-leaf"}):
                product_id = article.get("data-test-key")
                if product_id:
                    yield self.product(
                        product_id=product_id,
                    )

    def product(self, product_id: str) -> LegoProduct:
        """Get a product"""

        return LegoProduct(
            lego_api=self._lego_api,
            lego_store=self,
            product_id=product_id,
        )

    def new_products(self) -> Generator[LegoProduct, None, None]:
        """Get new products"""

        yield from self.get_list_page(
            path=f"{self.base_url}/categories/new-sets-and-products",
        )

    @property
    def themes(self) -> list[str]:
        """Get all themes"""

        soup = self._lego_api.get_page(
            path=f"{self.base_url}/themes",
        )

        found_themes = set()
        for theme in soup.select("main article>a"):
            found_themes.add(theme.get("href").split("/")[-1])

        return found_themes

    def products_from_theme(self, theme) -> Generator[LegoProduct, None, None]:
        """Get products from a theme"""

        yield from self.get_list_page(
            path=f"{self.base_url}/themes/{theme}",
        )
