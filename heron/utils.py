import warnings


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
