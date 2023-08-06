from enum import Enum


class SupportedPages(Enum):
    """
    List of pages which is able to parse by this module
    """
    LECTURE_INFORMATION = 'https://portal.student.kit.ac.jp/ead/?c=lecture_information'
    LECTURE_CANCELLATION = 'https://portal.student.kit.ac.jp/ead/?c=lecture_cancellation'
    NEWS = 'https://portal.student.kit.ac.jp/'
