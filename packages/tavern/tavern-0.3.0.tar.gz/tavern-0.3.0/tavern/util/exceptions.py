class TavernException(Exception):
    pass


class BadSchemaError(TavernException):
    """Schema mismatch
    """
    pass


class TestFailError(TavernException):
    """Test failed somehow
    """
    pass


class UnexpectedKeysError(TavernException):
    """Unexpected keys used in request specification
    """
    pass


class MissingFormatError(TavernException):
    """Tried to use a variable in a format string but it was not in the
    available variables
    """
    pass


class MissingCookieError(TavernException):
    """Tried to use a cookie in a request that was not present in the session
    cookie jar
    """
    pass
