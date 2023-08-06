import os
import unittest
import codecs

from datetime import datetime
from nose.tools import ok_, eq_
from student_portal_crawler.parser import NewsParser


class NewsParserTest(unittest.TestCase):
    """Test case for NewsParser"""

    SAMPLE_DATE = datetime(2018, 2, 9)
    RESULT_DATA_SET = [
        {
            'created_at': SAMPLE_DATE,
            'division': '〈学務課〉',
            'category': '《その他》',
            'detail': 'PDFのお知らせ\nお知らせ一行目\nお知らせ二行目',
            'title': 'PDFのお知らせ',
            'links': [
                {
                    'title': 'PDFのお知らせ',
                    'url': 'https://example.com/example.pdf'
                }
            ]
        },
        {
            'created_at': SAMPLE_DATE,
            'division': '〈学務課〉',
            'category': '《その他》',
            'detail': '普通のリンクのお知らせ\nお知らせ一行目\nお知らせ二行目',
            'title': '普通のリンクのお知らせ',
            'links': [
                {
                    'title': '普通のリンクのお知らせ',
                    'url': 'https://example.com/'
                }
            ]
        },
        {
            'created_at': SAMPLE_DATE,
            'division': '〈学務課〉',
            'category': '《その他》',
            'detail': 'リンク無しお知らせ\nお知らせ一行目\nお知らせ二行目',
            'title': 'リンク無しお知らせ',
            'links': []
        },
    ]

    @classmethod
    def setUpClass(cls):
        sample_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'samples')
        with codecs.open(os.path.join(sample_dir_path, 'news.html'), 'r', encoding='utf-8') as fp:
            cls.HTML = fp.read()

    def test_normal_response(self):
        """Normal response test for NewsParser"""
        parser = NewsParser(self.HTML)
        data = parser.parse()
        ok_(type(data), dict)
        ok_('data' in data.keys())
        eq_(len(data['data']), 3)
        for expected_result, actual_result in zip(self.RESULT_DATA_SET, data['data']):
            eq_(expected_result, actual_result)

    def test_empty_response(self):
        """Empty response test for NewsParser"""
        parser = NewsParser('')
        data = parser.parse()
        ok_(type(data), dict)
        ok_('data' in data.keys())
        eq_(len(data['data']), 0)
