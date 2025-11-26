import pytest
from logging import getLogger

from bs4 import BeautifulSoup

from lego_store_availability import LegoAPI, LegoStore, LegoProduct

logger = getLogger(__name__)

@pytest.fixture
def lego():
  return LegoAPI()

def test_store_product(lego):
    store = lego.store(
        lang="fr-fr",
    )

    product = store.product(
        product_id="10307",
    )

    assert isinstance(product, LegoProduct)
    assert product.product_id == "10307"

def test_store_new_products(lego):
    store = lego.store(
        lang="fr-fr",
    )

    products = store.new_products()
    # Assert that the generator contains at least one product
    first_product = next(products)
    assert isinstance(first_product, LegoProduct)


def test_store_theme(lego):
    store = lego.store(
        lang="fr-fr",
    )

    themes = store.themes
    assert isinstance(themes, set)
    assert len(themes) > 0
    assert isinstance(themes.pop(), str)


def test_store_products_from_theme(lego):
    store = lego.store(
        lang="fr-fr",
    )

    products = store.products_from_theme(
        theme="brickheadz",
    )
    # Assert that the generator contains at least one product
    first_product = next(products)
    assert isinstance(first_product, LegoProduct)


def test_store_products_from_fetched_theme(lego):
    store = lego.store(
        lang="fr-fr",
    )

    products = store.products_from_theme(
        theme=store.themes.pop(),
    )
    # Assert that the generator contains at least one product
    first_product = next(products)
    assert isinstance(first_product, LegoProduct)