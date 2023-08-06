class BaseUrl2VApiException(Exception):
    pass


class InvalidUrlPattern(BaseUrl2VApiException):
    pass


class UnrecognisedProtocol(BaseUrl2VApiException):
    pass


class InvalidInputPattern(BaseUrl2VApiException):
    pass
