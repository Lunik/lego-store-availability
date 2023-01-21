import sys
import yaml
from yaml.loader import SafeLoader

from lego_store_availability import Store, LegoAPI

def usage(argv):
  print(f"  Usage: {argv[0]} <CONFIG_FILE>")


if __name__ == "__main__":
  if len(sys.argv) != 2:
    usage(sys.argv)
    sys.exit(1)

  with open(sys.argv[1], 'r', encoding="UTF-8") as f:
    config = yaml.load(f, Loader=SafeLoader)

  api = LegoAPI(**config["api"])
  store = Store(api=api, **config["store"])

  for product in store.get_brickheadz():
    print(product.name, "==>", product.availability)
