import re

from bs4 import BeautifulSoup
from requests import Session

HTTP_SESSION = Session()
HTTP_SESSION.headers.update({"User-Agent": "Lunik/lego-store-availability"})

NAME_REGEX = re.compile(r"^[^|]+")

class Product:
  name = None
  availability = None

  def __init__(self, item_id):
    self.item_id = item_id


  @staticmethod
  def _request_page(url):
    response = HTTP_SESSION.get(url)

    response.raise_for_status()

    return response.content.decode("UTF-8")


  @staticmethod
  def _parse_page(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")

    product_metas = soup.head.find_all(
      lambda el:
        el.name == "meta" and el.has_attr("property") and el["property"] == "og:title"
    )
    availability_metas = soup.head.find_all(
      lambda el:
        el.name == "meta" and el.has_attr("property") and el["property"] == "product:availability"
    )

    if len(product_metas) <= 0:
      raise Exception("No meta tag found. Unable to get product title")

    if len(availability_metas) <= 0:
      raise Exception("No meta tag found. Unable to get availability")

    name = NAME_REGEX.search(product_metas[0]["content"]).group(0).strip()
    availability = availability_metas[0]["content"]

    return (name, availability)


  def load(self, store):
    product_url = f"{store.base_url}/product/{self.item_id}"

    raw_page = Product._request_page(product_url)

    self.name, self.availability = Product._parse_page(raw_page)
