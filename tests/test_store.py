from lego_store_availability import Store

def test_baseurl_01():
  store = Store()

  assert store.base_url == "https://www.lego.com/fr-fr"

def test_baseurl_02():
  store = Store(lang="en-us")

  assert store.base_url == "https://www.lego.com/en-us"

def test_baseurl_03():
  store = Store(insecure=True)

  assert store.base_url == "http://www.lego.com/fr-fr"
