from datetime import datetime
from typing import Type
from .shibboleth_login import ShibbolethClient
from .parser import REGISTERED_PARSERS, get_key_from_url, GeneralParser, SupportedPages, BaseParser
from .page import Page


class PortalBrowser(object):
    """Wrapper class for crawling Portal website"""

    def __init__(self, username: str, password: str):
        """
        Init instance
        :param username: your student id such as 'b0000000'
        :param password: password for your student id
        """
        self._username = username
        self._password = password
        self._client = ShibbolethClient(self._username, self._password)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._client.close()

    def get_page(self, url: str, **kwards) -> Page:
        """
        Get `Page` object by url.
        :param url: str
        :param kwards: option for `requests.Session.get`
        :return: `Page` object
        """
        key = get_key_from_url(url)
        if key not in REGISTERED_PARSERS:
            parser = GeneralParser
        else:
            parser = REGISTERED_PARSERS[key]
        return self._get_page(url, parser, **kwards)

    def get_lecture_information(self, **kwards) -> Page:
        """
        Get lecture information from 'https://portal.student.kit.ac.jp/ead/?c=lecture_information'
        :param kwards: option for `requests.Session.get`
        :return: `Page` object
        """
        url = SupportedPages.LECTURE_INFORMATION.value
        return self._get_page(url, REGISTERED_PARSERS[url], **kwards)

    def get_lecture_cancellation(self, **kwards) -> Page:
        """
        Get lecture information from 'https://portal.student.kit.ac.jp/ead/?c=lecture_cancellation'
        :param kwards: option for `requests.Session.get`
        :return: `Page` object
        """
        url = SupportedPages.LECTURE_CANCELLATION.value
        return self._get_page(url, REGISTERED_PARSERS[url], **kwards)

    def get_news(self, **kwards) -> Page:
        """
        Get news from 'https://portal.student.kit.ac.jp/'
        :param kwards: option for `requests.Session.get`
        :return: `Page` object
        """
        url = SupportedPages.NEWS.value
        return self._get_page(url, REGISTERED_PARSERS[url], **kwards)

    def _get_page(self, url: str, parser: Type[BaseParser], **kwards) -> Page:
        """
        Get response from web, and return instance of `Page`
        :param url: target page
        :param parser: parser for above page
        :param kwards: option for `requests.Session.get`
        :return: `Page` object
        """
        return Page(response=self._client.get(url, **kwards), parser=parser, access_at=datetime.now())
