import os
import pytest
import responses
import requests

from lego_store_availability import Product, Store, LegoAPI

RESOURCES_DIR = f"{os.path.dirname(os.path.realpath(__file__))}/resources"

@pytest.fixture
def store():
  api = LegoAPI(cache_type='memory')

  return Store(api)


@responses.activate
def test_product_01(store):
  api = LegoAPI(cache_type='memory')

  with open(
    f"{RESOURCES_DIR}/doctor-who-21304-FULL-OUT.html",
    'r', encoding="UTF-8"
  ) as file:
    responses.add(responses.GET, "https://www.lego.com/fr-fr/product/doctor-who-21304",
      body=file.read(), status=200)

  product = Product(api, item_id="doctor-who-21304")

  product.load(store)

  assert product.name == "Doctor Who 21304"
  assert product.availability == "out of stock"
  assert product.product_url == "https://www.lego.com/fr-fr/product/doctor-who-21304"
  assert product.item_id == "doctor-who-21304"
  assert product.retailer_item_id == "21304"


@responses.activate
def test_product_02(store):
  api = LegoAPI(cache_type='memory')

  with open(
    f"{RESOURCES_DIR}/doctor-who-21304-FULL-IN.html",
    'r', encoding="UTF-8"
  ) as file:
    responses.add(responses.GET, "https://www.lego.com/fr-fr/product/doctor-who-21304",
      body=file.read(), status=200)

  product = Product(api, item_id="doctor-who-21304")

  product.load(store)

  assert product.name == "Doctor Who 21304"
  assert product.availability == "in stock"
  assert product.product_url == "https://www.lego.com/fr-fr/product/doctor-who-21304"
  assert product.item_id == "doctor-who-21304"
  assert product.retailer_item_id == "21304"


@responses.activate
def test_product_03(store):
  api = LegoAPI(cache_type='memory')

  with open(
    f"{RESOURCES_DIR}/doctor-who-21304-MISSING-NAME.html",
    'r', encoding="UTF-8"
  ) as file:
    responses.add(responses.GET, "https://www.lego.com/fr-fr/product/doctor-who-21304",
      body=file.read(), status=200)

  product = Product(api, item_id="doctor-who-21304")

  with pytest.raises(Exception):
    product.load(store)


@responses.activate
def test_product_04(store):
  api = LegoAPI(cache_type='memory')

  with open(
    f"{RESOURCES_DIR}/doctor-who-21304-MISSING-AVAILABILITY.html",
    'r', encoding="UTF-8"
  ) as file:
    responses.add(responses.GET, "https://www.lego.com/fr-fr/product/doctor-who-21304",
      body=file.read(), status=200)

  product = Product(api, item_id="doctor-who-21304")

  product.load(store)

  assert product.availability is None


@responses.activate
def test_product_05(store):
  api = LegoAPI(cache_type='memory')

  responses.add(responses.GET, "https://www.lego.com/fr-fr/product/doctor-who-21304",
      status=404)

  product = Product(api, item_id="doctor-who-21304")

  with pytest.raises(requests.exceptions.HTTPError):
    product.load(store)
