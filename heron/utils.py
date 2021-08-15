import warnings
from datetime import datetime


def to_dollars(cents):
    if cents is None:
        return cents

    if isinstance(cents, str) and "." not in cents:
        dollars = float(cents) / 100.0
    elif isinstance(cents, int):
        dollars = cents / 100.0
    elif isinstance(cents, float):
        warnings.warn("assuming float value is already in dollars", UserWarning)
        dollars = cents

    else:
        raise ValueError(f"cannot convert {cents} cents to dollars")

    return round(dollars, 2)


def to_iso_format(d):
    if isinstance(d, int):
        return datetime.fromtimestamp(d).isoformat()

    if isinstance(d, str) and d.isdigit():
        return datetime.fromtimestamp(int(d)).isoformat()

    try:
        datetime.strptime(d, "%Y-%m-%dT%H:%M:%S")
    except TypeError:
        pass
    else:
        return d

    raise ValueError(f"cannot convert {d} to ISO format")
