"""
Lego Product
"""

import re
from logging import getLogger

logger = getLogger(__name__)

NAME_REGEX = re.compile(r"^[^|]+")


class LegoProduct:
    """Lego Product"""

    _meta_attributes = {
        "og:title": "title",
        "og:description": "description",
        "og:image": "image_url",
        "og:url": "url",
        "product:brand": "brand",
        "product:availability": "availability",
        "product:condition": "condition",
        "product:price:amount": "price",
        "product:price:currency": "currency",
        "product:retailer_item_id": "retailer_item_id",
    }

    def __init__(self, lego_api: "LegoAPI", lego_store: "LegoStore", product_id: str):
        self._lego_api = lego_api
        self._lego_store = lego_store
        self.product_id = product_id

        self._fetch()

    def __repr__(self):
        return f"<LegoProduct {self.product_id}>"

    @property
    def name(self):
        """Returns the name of the product by stripping it from the title"""
        if hasattr(self, "title"):
            return NAME_REGEX.match(self.title).group(0).strip()

        return None

    def _fetch(self):
        soup = self._lego_api.get_page(
            path=f"{self._lego_store.base_url}/product/{self.product_id}"
        )

        for header in soup.head.find_all("meta"):

            meta_property = header.get("property")
            if meta_property in self._meta_attributes:
                setattr(
                    self, self._meta_attributes[meta_property], header.get("content")
                )
