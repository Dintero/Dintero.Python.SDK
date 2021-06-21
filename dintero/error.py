class DinteroException(Exception):
    def __init__(self, message, status_code, headers, body):
        self.message = message
        self.status_code = status_code
        self.headers = headers
        self.body = body

    def __str__(self):
        return self.message + " " + str(self.status_code) + " " + self.body


class AuthError(DinteroException):
    pass


class InvalidRequestBody(DinteroException):
    pass


class UnexpectedError(DinteroException):
    pass


class DinteroClientError(Exception):
    pass


class InvalidFieldError(DinteroClientError):
    def __init__(self, message, field):
        self.message = message
        self.field = field

    def __str__(self):
        return self.message + " " + str(self.field)
