from .base import BaseParser, GeneralParser, REGISTERED_PARSERS
from .static import SupportedPages
from .utils import norm, get_key_from_url

from .lec_info import LectureInformationParser
from .lec_cancel import LectureCancellationParser
from .news import NewsParser
