import os
import pytest
from logging import getLogger

from bs4 import BeautifulSoup

from lego_store_availability import LegoAPI, LegoStore, LegoProduct

logger = getLogger(__name__)


@pytest.fixture
def store():
    return LegoAPI().store(
        lang="fr-fr",
    )


@pytest.mark.skipif(os.environ.get("CI") == "true", reason="Skip in CI")
def test_store_product(store):
    product = store.product(
        product_id="10307",
    )

    assert isinstance(product, LegoProduct)
    assert product.product_id == "10307"
    assert product.name == "La tour Eiffel 10307"
    assert product.title
    assert product.description
    assert product.image_url
    assert product.url
    assert product.brand
    assert product.availability
    assert product.condition
    assert product.price
    assert product.currency
    assert product.retailer_item_id
