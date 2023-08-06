from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock
from nose.tools import eq_, raises

from student_portal_crawler import ParseError
from student_portal_crawler.page import Page


class TestPage(TestCase):
    """Test case for `base.Page`"""

    def setUp(self):
        self.sample_date = datetime.strptime('2018/3/31', '%Y/%m/%d')
        self.sample_response = MagicMock(
            text='',
            status_code=200,
            url='https://www.example.com/'
        )
        self.sample_parser = MagicMock(
            return_value=MagicMock(
                data={'data': ''},
                soup='soup'
            )
        )

    def test_check_params(self):
        """Parameters validation test for `base.Page`"""
        page = Page(self.sample_response, self.sample_parser, self.sample_date)
        eq_(page.url, self.sample_response.url)
        eq_(page.html, self.sample_response.text)
        eq_(page.status_code, self.sample_response.status_code)
        eq_(page.as_dict, self.sample_parser().data)
        eq_(page.soup, self.sample_parser().soup)
        eq_(page.access_at, self.sample_date)

    @raises(ParseError)
    def test_parse_error(self):
        """Error response test for `base.Page`"""
        self.sample_response.status_code = 404
        page = Page(self.sample_response, self.sample_parser, self.sample_date)
        eq_(page.url, self.sample_response.url)
        eq_(page.html, self.sample_response.text)
        eq_(page.status_code, self.sample_response.status_code)
        eq_(page.soup, self.sample_parser().soup)
        eq_(page.access_at, self.sample_date)
        page.as_dict
