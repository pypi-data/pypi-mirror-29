# Cachalot [![PyPI version](https://badge.fury.io/py/cachalot.svg)](https://badge.fury.io/py/cachalot) [![Pipeline status](https://gitlab.com/radek-sprta/cachalot/badges/master/pipeline.svg)](https://gitlab.com/radek-sprta/cachalot/commits/master) [![Coverage report](https://gitlab.com/radek-sprta/cachalot/badges/master/coverage.svg)](https://gitlab.com/radek-sprta/cachalot/commits/master)

Cachalot is a minimal persistent memoization cache. It provides a decorator, that stores function result for future use. Perfect for heavy computations and I/O operation (such as web requests). On backend, it uses TinyDB for storage.

## Features
- Simple usage via decorator
- Persistent caching
- Key expiration
- Maximum cache size, to prevent bloat

## Installation
Cachalot requires Python 3.5 or newer to run.

**Python package**

You can easily install Cachalot using pip:

`pip3 install cachalot`

**Manual**

Alternatively, to get the latest development version, you can clone this repository and then manually install it:

```
git clone git@gitlab.com:radek-sprta/cachalot.git
cd cachalot
python3 setup.py install
```

## Usage
```python
from cachalot import Cache

@Cache()
def expensive_function():
    return expensive_calculation()
```

### Advanced usage
```python
from cachalot import Cache

@Cache(path='cache.json', timeout=3600, size=5000)
def expensive_function():
    return expensive_calculation()
```

- `path`: Path to the database file. Defaults to .cache.json.
- `timeout`: How long should the data be cached in seconds. Defaults to 86400 (1 day).
- `size`: Maximum number of keys cached. Defaults to 10000.

For more information, see [documentation][documentation].

## TODO
- Test suite
- Optionally retry if blank data is returned

## Contributing
For information on how to contribute to the project, please check the [Contributor's Guide][contributing]

## Contact
[mail@radeksprta.eu](mailto:mail@radeksprta.eu)

[incoming+radek-sprta/cachalot@gitlab.com](incoming+radek-sprta/cachalot@gitlab.com)

## License
MIT License

## Credits
This package was created with [Cookiecutter][cookiecutter] and the [python-cookiecutter][python-cookiecutter] project template. Inspired by [Cashier][cachier]

[cachier]: https://github.com/atmb4u/cashier
[contributing]: https://gitlab.com/radek-sprta/cachalot/blob/master/CONTRIBUTING.md
[cookiecutter]: https://github.com/audreyr/cookiecutter
[documentation]: https://radek-sprta.gitlab.io/cachalot
[python-cookiecutter]: https://gitlab.com/radek-sprta/python-cookiecutter
