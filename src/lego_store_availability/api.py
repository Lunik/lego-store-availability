from importlib import import_module
from logging import getLogger

from bs4 import BeautifulSoup
from requests_cache import CachedSession

logger = getLogger(__name__)

cache_backend = dict(
  sqlite='sqlite',
  memory='memory',
  s3=lambda: getattr(import_module('.cache', package='lego_store_availability'), 'S3Cache')
)

class LegoAPI:
  supported_cache_backend = ['sqlite', 'memory', 's3']

  def __init__(self, cache_type="memory", cache_opts=None):
    if cache_type not in self.supported_cache_backend:
      raise Exception(f"Unsuported cache. Available {', '.join(self.supported_cache_backend)}")

    backend = cache_backend[cache_type]
    if not isinstance(backend, str):
      if cache_opts is None:
        cache_opts = {}
      backend = backend()(**cache_opts)

    self.session = CachedSession('lego-store-availability', backend=backend, use_cache_dir=True)
    self.session.cache.responses.is_binary = True
    self.session.headers.update({"User-Agent": "Lunik/lego-store-availability"})


  def request_page(self, url):
    logger.debug("Requesting page with url '%s'", url)
    response = self.session.get(url)

    response.raise_for_status()

    return BeautifulSoup(response.content.decode("UTF-8"), "html.parser")

  @staticmethod
  def find_meta_header(soup, property_name):
    res = soup.head.find_all(
      lambda el:
        el.name == "meta" and el.has_attr("property") and el["property"] == property_name
    )

    if len(res) <= 0:
      print(f"No meta tag found. Unable to get {property_name}")
      return None

    return res[0]["content"]

  @staticmethod
  def find_element_from_selector(soup, el_type, attrs=None, multi=False):
    if attrs is None:
      attrs = {}

    if multi:
      return soup.find_all(el_type, attrs)

    return soup.find(el_type, attrs)
