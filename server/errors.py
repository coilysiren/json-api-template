"""
errors.py lists all the custom errors that can be returned by our server
"""


class ErrorWithStatus(BaseException):
    """
    ErrorWithStatus is a base class used to help other errors have consistent `status_code` variable
    """

    status_code: int


class InvalidUserInput(ErrorWithStatus):
    """
    InvalidUserInput is returned when our client had invalid input
    """

    status_code = 400


class NotFound(ErrorWithStatus):
    """
    NotFound is returned when a given resource could not be found
    """

    status_code = 404


class ServerError(ErrorWithStatus):
    """
    ServerError is returned when there was an unknown error
    these should generally by caught, and page somebody
    """

    status_code = 500
