import re
from logging import getLogger

from .api import LegoAPI

logger = getLogger(__name__)

NAME_REGEX = re.compile(r"^[^|]+")

class Product:
  name = None
  description = None
  image_url = None
  availability = None
  product_url = None
  product_uri = None
  item_id = None
  retailer_item_id = None
  price = None

  def __init__(self, api, item_id=None, product_uri=None):
    self.api = api

    self.item_id = item_id
    self.product_uri = product_uri

  @staticmethod
  def _parse_page(soup):
    title = LegoAPI.find_meta_header(soup, "og:title")
    description = LegoAPI.find_meta_header(soup, "og:description")
    image_url = LegoAPI.find_meta_header(soup, "og:image")
    availability = LegoAPI.find_meta_header(soup, "product:availability")
    price_amount = LegoAPI.find_meta_header(soup, "product:price:amount")
    price_currency = LegoAPI.find_meta_header(soup, "product:price:currency")
    retailer_item_id = LegoAPI.find_meta_header(soup, "product:retailer_item_id")

    name = NAME_REGEX.search(title).group(0).strip()
    price = f"{price_amount} {price_currency}"

    return (name, description, image_url, availability, price, retailer_item_id)

  def load(self, store):
    if self.product_uri:
      self.product_url = f"{store.root_url}/{self.product_uri}"
    else:
      self.product_url = f"{store.base_url}/product/{self.item_id}"

    logger.debug("Loading product at '%s'", self.product_url)

    soup = self.api.request_page(self.product_url)

    (self.name, self.description, self.image_url,
    self.availability, self.price, self.retailer_item_id) = Product._parse_page(soup)
