# LEGO™ store availability

Check the availability of Lego™ product in stores.

## Disclamer

This tools is not related in any way to LEGO™ and all of it's trademark.

This tools is not designed for malicious usage and any individual or group using it this way is responsible for is own actions.

## Install

```shell
pip3 install lego-store-availability
```

## Usage

First you need to create a `Store` object :

```python
from lego_store_availability import Store

store = Store(lang="fr-fr")
```

Then request a `Product` :

```python
from lego_store_availability import Product

product = Product(id="ahsoka-tano-40539")

product.load(store)

print(product.name, product.availability)
```

### Example

You can use the example in [example folder](./example) :
```shell
PYTHONPATH=src/ python3 example/main.py example/config.yml
```
Result :
```shell
Le Taj Mahal 21056 ==> in stock
Ahsoka Tano™ 40539 ==> out of stock
Doctor Who 21304   ==> out of stock
```

## Contribute

- Clone or fork the repository.
- Install dev dependencies with `pip3 install -r dev-requirements.txt`
- Develop your feature or fix
- Lint with [pylint](https://pylint.pycqa.org/en/latest/)
- Test it with [pytest](https://pytest.org) under [tests/](./tests) directory
  - Mock HTTP requests with [responses](https://github.com/getsentry/responses)
- Push & create a Pull Request on `develop` branch
- Wait for the CI (Github Action) to exit in success state