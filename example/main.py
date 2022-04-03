import sys
import yaml
from yaml.loader import SafeLoader

from lego_store_availability import Store, Product

def usage(argv):
  print(f"  Usage: {argv[0]} <CONFIG_FILE>")


if __name__ == "__main__":
  if len(sys.argv) != 2:
    usage(sys.argv)
    sys.exit(1)

  config_file = sys.argv[1]

  with open(config_file, 'r', encoding="UTF-8") as f:
    config = yaml.load(f, Loader=SafeLoader)

  store = Store(**config["store"])

  for item_cfg in config["products"]:
    product = Product(**item_cfg)

    product.load(store)

    print(product.name, "==>", product.availability)
