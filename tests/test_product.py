import pytest
import responses
import os
import requests

from lego_store_availability import Product,Store

@pytest.fixture
def store():
  return Store()


@responses.activate
def test_product_01(store):
  with open(f"{os.path.dirname(os.path.realpath(__file__))}/resources/doctor-who-21304-FULL-OUT.html", 'r') as f:
    responses.add(responses.GET, "https://www.lego.com/fr-fr/product/doctor-who-21304",
      body=f.read(), status=200)

  product = Product(id="doctor-who-21304")

  product.load(store)

  assert product.name == "Doctor Who 21304"
  assert product.availability == "out of stock"

@responses.activate
def test_product_02(store):
  with open(f"{os.path.dirname(os.path.realpath(__file__))}/resources/doctor-who-21304-FULL-IN.html", 'r') as f:
    responses.add(responses.GET, "https://www.lego.com/fr-fr/product/doctor-who-21304",
      body=f.read(), status=200)

  product = Product(id="doctor-who-21304")

  product.load(store)

  assert product.name == "Doctor Who 21304"
  assert product.availability == "in stock"

@responses.activate
def test_product_03(store):
  with open(f"{os.path.dirname(os.path.realpath(__file__))}/resources/doctor-who-21304-MISSING-NAME.html", 'r') as f:
    responses.add(responses.GET, "https://www.lego.com/fr-fr/product/doctor-who-21304",
      body=f.read(), status=200)

  product = Product(id="doctor-who-21304")

  with pytest.raises(Exception):
    product.load(store)

@responses.activate
def test_product_04(store):
  with open(f"{os.path.dirname(os.path.realpath(__file__))}/resources/doctor-who-21304-MISSING-AVAILABILITY.html", 'r') as f:
    responses.add(responses.GET, "https://www.lego.com/fr-fr/product/doctor-who-21304",
      body=f.read(), status=200)

  product = Product(id="doctor-who-21304")

  with pytest.raises(Exception):
    product.load(store)

@responses.activate
def test_product_05(store):
  responses.add(responses.GET, "https://www.lego.com/fr-fr/product/doctor-who-21304",
      status=404)

  product = Product(id="doctor-who-21304")

  with pytest.raises(requests.exceptions.HTTPError):
    product.load(store)