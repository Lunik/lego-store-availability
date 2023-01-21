from lego_store_availability import Store, LegoAPI

api = LegoAPI(cache_type='memory')

def test_baseurl_01():
  store = Store(api)

  assert store.base_url == "https://www.lego.com/fr-fr"

def test_baseurl_02():
  store = Store(api, lang="en-us")

  assert store.base_url == "https://www.lego.com/en-us"

def test_baseurl_03():
  store = Store(api, insecure=True)

  assert store.base_url == "http://www.lego.com/fr-fr"
