class Error(Exception):
    """Base error class for student_portal_crawler"""
    pass


class ParseError(Error):
    """Could not parse error"""
    pass
