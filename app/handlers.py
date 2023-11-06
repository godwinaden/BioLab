from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from app.utils import log
from app import exceptions

def flight_exception_handler(request: Request, exc: exceptions.FlightException | HTTPException):
	base_error_message = f"Execution Failed: {request.method}: {request.url}"
	msg = f"{base_error_message}. Detail: {exc.msg}"
	log(msg=msg, level=40, exc=exc.error)
	return JSONResponse(status_code=exc.status_code, content={"message": msg})


def credential_exception_handler(request: Request, exc: exceptions.CredentialsExistException):
	flight_exception_handler(request, exc)


def no_credential_exception_handler(request: Request, exc: exceptions.CredentialsNotFoundException):
	flight_exception_handler(request, exc)


def invalid_city_name_handler(request: Request, exc: exceptions.InvalidCityNameException):
	flight_exception_handler(request, exc)


def invalid_city_code_handler(request: Request, exc: exceptions.InvalidCityCodeException):
	flight_exception_handler(request, exc)


def login_needed_handler(request: Request, exc: exceptions.LoginRequiredException):
	flight_exception_handler(request, exc)
