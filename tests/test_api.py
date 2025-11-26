from logging import getLogger

from bs4 import BeautifulSoup

from lego_store_availability import LegoAPI, LegoStore

logger = getLogger(__name__)

def test_base_api():
    lego = LegoAPI()

    result = lego.get_page()

    assert isinstance(result, BeautifulSoup)
    assert "LEGO" in result.title.text

def test_api_store():
    lego = LegoAPI()

    store = lego.store(
        lang="fr-fr",
    )

    assert isinstance(store, LegoStore)
    assert store.lang == "fr-fr"