# Heron Python Library

The Heron Python library provides easy access to the Heron Data API from
applications written in Python.

## Documentation

See the [OpenAPI Docs](https://app.herondata.io/docs).

## Installation

If you just want to use the package, just run:

```sh
pip install --upgrade heron
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
import heron

heron.basic_auth_username = "your-username"
heron.basic_auth_password = "super-random-password"

# optionally, specify the provider pull bank data from, in lowercase
heron.data_source = "plaid"
```

Then you can issue API requests using Python classes:

```python
end_user = heron.EndUser.create(...)

transactions = heron.Transaction.create_many([...])
```

You can see a longer example in the `examples/` directory.
