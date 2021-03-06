[![Lint and Test](https://github.com/heron-data/client-python/actions/workflows/lint_and_test.yml/badge.svg)](https://github.com/heron-data/client-python/actions/workflows/lint_and_test.yml)

# Heron Python

This library provides easy access to the [Heron Data](https://www.herondata.io)
API for applications written in Python.

![Demo GIF](https://user-images.githubusercontent.com/16668651/129679702-f9c1ae2d-66ec-43e1-818f-0f1d539ba348.gif)

## Documentation

No language-specific docs are currently maintained. For documentation on the
raw REST API this library uses behind the scenes, see our [OpenAPI
Docs](https://app.herondata.io/docs).

## Installation

If you just want to use the package, just run:

```sh
pip install --upgrade heron-data
```

Install from source with:

```sh
python setup.py install
```

### Requirements

-   Python 3.8+

## Usage

Import the `heron` package and set your config:

```python
import os

import heron

heron.basic_auth_username = os.getenv("HERON_USERNAME")
heron.basic_auth_password = os.getenv("HERON_PASSWORD")

# Experimental: if you pull from a fintech API, specify it here to get
# automatic conversion into a Heron Data API format. Supported: plaid,
# finicity, yodlee, truelayer
heron.provider = "plaid"
```

Alternatively, set `HERON_USERNAME` and `HERON_PASSWORD` as environment
variables which will be automatically picked up.

Then you can issue API requests using Python classes:

```python
end_user = heron.EndUser.create(...)

transactions = heron.Transaction.create_many([...])
```

You can see a longer example in the `examples/` directory.

## Contributing

Fork this repository, and install dev dependencies:

```
pip install -r requirements.dev.txt
```

Run tests and capture coverage with:

```
coverage run -m unittest
```

See test coverage with:

```
coverage report
```

Run linting with `flake8` and `black`:

```
flake8 . && black .
```

Submit a PR against the `main` branch and it will be reviewed.
