from fastapi import HTTPException


class FlightException(HTTPException):
    def __init__(self, status_code: int, msg: str, err: Exception = None):
        self.status_code = status_code
        self.msg = msg
        self.error = err


class CredentialsExistException(HTTPException):
    def __init__(self, err: Exception = None):
        self.status_code = 400
        self.msg = "Credentails Already Exists"
        self.error = err


class CredentialsNotFoundException(HTTPException):
    def __init__(self, err: Exception = None):
        self.status_code = 204
        self.msg = "No Credentails Found"
        self.error = err


class InvalidCityCodeException(HTTPException):
    def __init__(self, err: Exception = None):
        self.status_code = 400
        self.msg = "Invalid City Code"
        self.error = err


class InvalidCityNameException(HTTPException):
    def __init__(self, err: Exception = None):
        self.status_code = 400
        self.msg = "Invalid City Name"
        self.error = err


class LoginRequiredException(HTTPException):
    def __init__(self, err: Exception = None):
        self.status_code = 401
        self.msg = "Unauthorized Entry"
        self.error = err
