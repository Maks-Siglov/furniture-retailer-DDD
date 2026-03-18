class BaseApplicationException(Exception): ...


class OutOfStock(BaseApplicationException):
    """Raised when we cannot allocate order line"""
