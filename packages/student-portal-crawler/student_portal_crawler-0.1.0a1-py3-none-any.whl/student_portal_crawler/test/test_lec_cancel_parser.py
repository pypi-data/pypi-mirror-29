import os
import unittest
import codecs

from datetime import datetime
from nose.tools import ok_, eq_
from bs4 import BeautifulSoup
from student_portal_crawler.parser import LectureCancellationParser


class LectureCancellationParserTest(unittest.TestCase):
    """Test case for LectureCancellationParser"""

    SAMPLE_DATE = datetime(2018, 2, 7)
    SAMPLE_CANCEL_DATE = datetime(2018, 2, 14)
    RESULT_DATA_SET = [
        {
            'grade': '学部',
            'lecture': '工繊応用',
            'instructor': '工繊一郎',
            'cancel_date': SAMPLE_CANCEL_DATE,
            'week': '水曜日',
            'period': '1',
            'detail': 'チョコレートが欲しいため',
            'created_at': SAMPLE_DATE,
            'links': []
        },
        {
            'grade': '学部',
            'lecture': '工繊実践',
            'instructor': '工繊二郎',
            'cancel_date': SAMPLE_CANCEL_DATE,
            'week': '集中',
            'period': '-',
            'detail': '私もチョコレートが欲しいためsample link',
            'created_at': SAMPLE_DATE,
            'links': [
                {
                    'title': 'sample link',
                    'url': 'https://example.com/'
                }
            ]
        },
    ]

    @classmethod
    def setUpClass(cls):
        sample_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'samples')
        with codecs.open(os.path.join(sample_dir_path, 'cancellation.html'), 'r', encoding='utf-8') as fp:
            cls.HTML = fp.read()

    def test_normal_response(self):
        """Normal response test for LectureInformationParser"""
        parser = LectureCancellationParser(self.HTML)
        data = parser.parse()
        ok_(type(data), dict)
        ok_('data' in data.keys())
        eq_(len(data['data']), 2)
        for expected_result, actual_result in zip(self.RESULT_DATA_SET, data['data']):
            eq_(expected_result, actual_result)

    def test_empty_response(self):
        """Empty response test for LectureInformationParser"""
        parser = LectureCancellationParser('')
        data = parser.parse()
        ok_(type(data), dict)
        ok_('data' in data.keys())
        eq_(len(data['data']), 0)
