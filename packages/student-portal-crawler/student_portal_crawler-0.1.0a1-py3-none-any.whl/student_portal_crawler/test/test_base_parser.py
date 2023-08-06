from unittest import TestCase
from nose.tools import ok_, eq_, raises

from student_portal_crawler.parser import GeneralParser, BaseParser, REGISTERED_PARSERS


class TestBaseParser(TestCase):
    """Test case for `base.BaseParser`"""

    def test_cls_variable(self):
        """Class variable validation test for `base.BaseParser`"""
        base = BaseParser('')
        expect_parser_lib = 'lxml'
        eq_(base.PARSER_LIB, expect_parser_lib)
        expect_url = '/'
        eq_(base.URL, expect_url)

    @raises(NotImplementedError)
    def test_not_impl(self):
        """Calling not implemented method test for `base.BaseParser`"""
        base = BaseParser('')
        base.parse()

    def test_not_register(self):
        """Check registration test for `base.BaseParser`"""
        for k, v in REGISTERED_PARSERS.items():
            ok_(v is not BaseParser)

    def test_inheritance(self):
        """Valid inheritance test for `base.BaseParser`"""
        class TestParser(BaseParser):
            URL = 'https://www.example.com'

            def parse(self):
                return dict({'data': 'value'})
        test_parser = TestParser('')
        eq_(REGISTERED_PARSERS[test_parser.URL], TestParser)
        ok_(hasattr(test_parser, 'data'))
        eq_(type(test_parser.data), dict)
        ok_(hasattr(test_parser, '_soup'))
        ok_(hasattr(test_parser, 'soup'))
        ok_(hasattr(test_parser, 'parse'))
        ok_(hasattr(test_parser, '_data_cache'))

    @raises(ValueError)
    def test_invalid_inheritance_invalid_url(self):
        """Invalid inheritance (invalid url param) test for `base.BaseParser`"""
        class UrlInvalidParser(BaseParser):
            URL = ''

            def parse(self):
                return dict()

    @raises(AttributeError)
    def test_invalid_inheritance_midding_url(self):
        """Invalid inheritance (missing url param) test for `base.BaseParser`"""
        class UrlInvalidParser(BaseParser):
            def parse(self):
                return dict()

    @raises(AttributeError)
    def test_invalid_inheritance_not_impl(self):
        """Invalid inheritance (not implement `parse`) test for `base.BaseParser`"""
        class ParseNotImplParser(BaseParser):
            URL = 'http://www.example.com/'


class TestGeneralParser(TestCase):
    """Test case for `base.GeneralParser`"""

    def test_cls_variable(self):
        """Class variable validation test for `base.GeneralParser`"""
        base = BaseParser('')
        expect_parser_lib = 'lxml'
        eq_(base.PARSER_LIB, expect_parser_lib)
        expect_url = '/'
        eq_(base.URL, expect_url)

    def test_not_register(self):
        """Check registration test for `base.GeneralParser`"""
        for k, v in REGISTERED_PARSERS.items():
            ok_(v is not BaseParser)

    def test_implemented_parse(self):
        """Check implementation of `parse` method test for `base.GeneralParser`"""
        general_parser = GeneralParser('')
        eq_({'data': ''}, general_parser.parse())
        ok_(hasattr(general_parser, 'data'))
        ok_(type(general_parser.data), dict)
        ok_(hasattr(general_parser, '_soup'))
        ok_(hasattr(general_parser, 'soup'))
        ok_(hasattr(general_parser, 'parse'))
        ok_(hasattr(general_parser, '_data_cache'))
