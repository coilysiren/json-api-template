class ErrorWithStatus(BaseException):
    status_code: int


class InvalidUserInput(ErrorWithStatus):
    status_code = 400


class NotFound(ErrorWithStatus):
    status_code = 404


class ServerError(ErrorWithStatus):
    status_code = 500
