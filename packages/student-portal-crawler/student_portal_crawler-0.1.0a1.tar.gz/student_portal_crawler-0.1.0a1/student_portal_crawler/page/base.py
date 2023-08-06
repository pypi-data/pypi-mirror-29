from typing import TYPE_CHECKING, Type
from student_portal_crawler.error import ParseError

if TYPE_CHECKING:
    from datetime import datetime
    from bs4 import BeautifulSoup
    from requests import Response
    from student_portal_crawler.parser import BaseParser


class Page(object):
    """General page class for Portal website"""

    def __init__(self, response: 'Response', parser: Type['BaseParser'], access_at: 'datetime'):
        self._response = response
        self._parser = parser(response.text)
        self._access_at = access_at

    @property
    def html(self) -> str:
        """
        html string of this page
        :return: str
        """
        return self._response.text

    @property
    def url(self) -> str:
        """
        url string of this page
        :return: str
        """
        return self._response.url

    @property
    def status_code(self) -> int:
        """
        status code when access to this page
        :return: int
        """
        return self._response.status_code

    @property
    def soup(self) -> 'BeautifulSoup':
        """
        html loaded by BeautifulSoup4
        :return: BeautifulSoup4
        """
        return self._parser.soup

    @property
    def access_at(self) -> 'datetime':
        """
        access time
        :return: datetime.datetime
        """
        return self._access_at

    @property
    def as_dict(self) -> dict:
        """
        page data which is converted into dictionary by parser
        :return: dict
        """
        if self.status_code > 400:
            raise ParseError('status_code is {}'.format(self.status_code))
        return self._parser.data

    def __repr__(self):
        return 'Page(url="{url}", parser={parser_cls}, access_at="{access_at}")'.format(
            url=self.url,
            parser_cls=self._parser.__class__.__name__,
            access_at=self.access_at
        )
