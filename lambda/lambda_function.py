import json
from lego_store_availability import Store, Product

def lambda_handler(event, context):
  # TODO implement

  store = Store(lang=event["lang"])

  result = []

  for item_id in event["products"]:
    product = Product(item_id)
    product.load(store)

    result.append(dict(
      name=product.name,
      availability=product.availability
    ))

  return result
