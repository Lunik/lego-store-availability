
from logging import getLogger

from .api import LegoAPI
from .product import Product

logger = getLogger(__name__)

class Store:
  hostname = "www.lego.com"

  def __init__(self, api, lang="fr-fr", insecure=False):
    self.api = api
    self.lang = lang
    self.insecure = insecure

  @property
  def root_url(self):
    protocol = "http" if self.insecure else "https"

    return f"{protocol}://{self.hostname}"

  @property
  def base_url(self):
    return f"{self.root_url}/{self.lang}"

  @property
  def new_url(self):
    return f"{self.base_url}/categories/new-sets-and-products"

  @property
  def brickheadz_url(self):
    return f"{self.base_url}/themes/brickheadz"

  @staticmethod
  def _parse_new_page(api, soup):
    #nav_previous = LegoAPI.find_element_from_selector(soup, 'a', {"rel": 'prev'})
    nav_next = LegoAPI.find_element_from_selector(soup, 'a', {"rel": 'next'})

    products_links = map(
      lambda el: LegoAPI.find_element_from_selector(el, 'a').get('href'),
      filter(
        lambda el: 'disruptor-positioner' not in el.get('class'),
        LegoAPI.find_element_from_selector(soup, 'li', {'data-test': 'product-item'}, multi=True)
      )
    )

    products = []
    for product_link in list(products_links):
      product = Product(api=api, product_uri=product_link)

      products.append(product)

    return (nav_next, products)

  def _parse_list_page(self, url):
    soup = self.api.request_page(url)

    products = []

    next_page, res = Store._parse_new_page(self.api, soup)
    products += res

    while next_page:
      soup = self.api.request_page(f"{self.root_url}/{next_page.get('href')}")
      next_page, res = Store._parse_new_page(self.api, soup)
      products += res

    product_total = len(products)
    logger.debug("Found %s products", product_total)

    for count, product in enumerate(products):
      logger.debug("Loading product (%s/%s)", count, product_total)
      try:
        product.load(self)
      except Exception as error:
        print(error)

    return products

  def get_new(self):
    return self._parse_list_page(self.new_url)

  def get_brickheadz(self):
    return self._parse_list_page(self.brickheadz_url)
