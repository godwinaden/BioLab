from fastapi import HTTPException


class BioException(HTTPException):
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


class InvalidFaceException(HTTPException):
    def __init__(self, err: Exception = None):
        self.status_code = 400
        self.msg = "Invalid Face"
        self.error = err


class InvalidFingerException(HTTPException):
    def __init__(self, err: Exception = None):
        self.status_code = 400
        self.msg = "Invalid Person"
        self.error = err


class LoginRequiredException(HTTPException):
    def __init__(self, err: Exception = None):
        self.status_code = 401
        self.msg = "Unauthorized Entry"
        self.error = err
