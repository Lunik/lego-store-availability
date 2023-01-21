import sys
import logging.config
import yaml
from yaml.loader import SafeLoader

from lego_store_availability import Store, LegoAPI

def usage(argv):
  print(f"  Usage: {argv[0]} <CONFIG_FILE>")

logging.config.dictConfig({
  'version': 1,
  'disable_existing_loggers': False,
  'formatters': {
    'standard': {
      'format': '[%(levelname)7s] %(name)35s: %(message)s'
    },
  },
  'loggers': {
    'lego_store_availability': {
      'level': 'DEBUG',
      'handlers': ['default'],
    },
  },
  'handlers': {
    'default': {
      'formatter': 'standard',
      'class': 'logging.StreamHandler',
      'stream': 'ext://sys.stdout',  # Default is stderr
    },
  },
})


if __name__ == "__main__":
  if len(sys.argv) != 2:
    usage(sys.argv)
    sys.exit(1)

  with open(sys.argv[1], 'r', encoding="UTF-8") as f:
    config = yaml.load(f, Loader=SafeLoader)

  api = LegoAPI(**config["api"])
  store = Store(api=api, **config["store"])

  for product in store.get_new():
    print(product.name, "==>", product.availability)
