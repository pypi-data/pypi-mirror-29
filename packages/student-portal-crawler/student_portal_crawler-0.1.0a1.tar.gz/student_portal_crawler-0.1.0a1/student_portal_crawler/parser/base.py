from typing import Dict, Type

from bs4 import BeautifulSoup

from .utils import get_key_from_url

REGISTERED_PARSERS = dict()  # type: Dict[str, Type['BaseParser']]


def install_parser(parser: 'BaseParser') -> None:
    """
    Register parser with its URL
    :param parser: a class inherited from `BaseParser`
    :return: None
    """
    dict_key = get_key_from_url(parser.URL)
    REGISTERED_PARSERS[dict_key] = parser


class AbstractParser(type):
    """Abstract class for `Parser`"""

    def __new__(mcs, name, bases, class_dict: dict):
        must_impl_vars = ['URL', 'parse']
        if bases != (object,):
            for must_impl_var in must_impl_vars:
                if must_impl_var not in class_dict.keys():
                    raise AttributeError('{cls} has no attribute {var}'.format(cls=name, var=must_impl_var))
        cls = type.__new__(mcs, name, bases, class_dict)  # type: BaseParser
        # URLとの関連付け
        if name not in ['BaseParser', 'GeneralParser']:
            install_parser(cls)
        return cls


class BaseParser(object, metaclass=AbstractParser):
    """Base parser class for Portal website"""

    PARSER_LIB = 'lxml'
    URL = '/'

    def __init__(self, html: str):
        self._soup = BeautifulSoup(html, self.PARSER_LIB)
        self._data_cache = dict()

    @property
    def soup(self) -> BeautifulSoup:
        """
        html loaded by BeautifulSoup4
        :return: BeautifulSoup4
        """
        return self._soup

    @property
    def data(self) -> dict:
        """
        Page data as dictionary
        :return: dict
        """
        if 'data' not in self._data_cache.keys():
            self._data_cache = self.parse()
        return self._data_cache

    def parse(self) -> dict:
        """
        Parse HTML and convert it to dict.
        :return: data as dict
        """
        raise NotImplementedError('This method must be implemented.')


class GeneralParser(BaseParser):
    """General parser for not supported pages"""
    URL = '/'

    def parse(self) -> dict:
        """
        Parser for not supported pages
        :return: { 'data': '' }
        """
        return {
            'data': ''
        }
