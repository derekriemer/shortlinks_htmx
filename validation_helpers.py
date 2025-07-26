import validators


def validate_url(url: str) -> True:
    if not validators.validate_url(url):
        raise ValueError(F"Invalid URL: {url}  is invalid.")
    return True
