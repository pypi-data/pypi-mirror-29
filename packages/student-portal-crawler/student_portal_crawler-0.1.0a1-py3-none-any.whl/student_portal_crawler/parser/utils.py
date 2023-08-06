from unicodedata import normalize
from urllib import parse


def norm(chars: str) -> str:
    """
    Return normalized characters via `unicodedata.normalize`
    :param chars: sentence
    :return: normalized sentence"""
    return normalize('NFKC', chars)


def get_key_from_url(url: str) -> str:
    """
    Normalize url in order to get unique key
    :param url: full url path
    :return: verified url
    """
    parsed = parse.urlparse(url)
    if len(parsed.scheme) == 0 or len(parsed.netloc) == 0:
        raise ValueError('URL should start from "http" or "https".')
    return url
