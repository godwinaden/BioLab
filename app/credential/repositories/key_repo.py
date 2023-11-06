from typing import Any
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette import status
from app.credential.schemas.key import KeyRequest
from app.database.models.credential_model import ApiCredential
from app.exceptions import CredentialsExistException, CredentialsNotFoundException, LoginRequiredException, \
	FlightException
from app.credential.schemas.key_response import DeletedKeyResponse


class KeyRepo:

	def create_credentials(self, request: Request, newKey: KeyRequest) -> Any:
		try:
			return ApiCredential.create_credentials(newKey)
		except Exception as e:
			return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": f"Bad Request: {e}"})

	def delete_credentials(self, request: Request, name: str, api_key) -> Any:
		try:
			if api_key:
				q, obj = ApiCredential.delete_credential(name)
				if q and obj is not None:
					return DeletedKeyResponse(app_key=obj["app_key"], app_name=name, )
				else:
					raise CredentialsNotFoundException()
			else:
				raise FlightException(
					status_code=403,
					msg="Could not validate credentials"
				)
		except Exception as e:
			return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": f"Bad Request: {e}"})

	def get_credentials(self, request: Request, name: str, api_key) -> Any:
		try:
			if api_key:
				q = ApiCredential.objects.filter(app_name=name)
				if q.count() >= 1:
					return q.first()
				else:
					raise CredentialsNotFoundException()
			else:
				raise FlightException(
					status_code=403,
					msg="Could not validate credentials"
				)
		except Exception as e:
			return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": f"Bad Request: {e}"})

	def get_all_credentials(self, request: Request, api_key):
		try:
			if api_key:
				q = ApiCredential.objects.all()
				if q.count() > 0:
					return [dict(x) for x in q]
				else:
					raise CredentialsNotFoundException()
			else:
				raise FlightException(
					status_code=401,
					msg="Could not validate Credentials"
				)
		except Exception as e:
			return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": f"Bad Request: {e}"})

	@staticmethod
	def verify_token(app_name: str, public_key: str) -> bool:
		try:
			q = ApiCredential.objects.filter(app_name=app_name)
			if q.count() > 0:
				obj = q.first()
				token = obj.public_key
				verified, msg = ApiCredential.verify_hash(token, public_key)
				return verified
			else:
				raise LoginRequiredException()
		except Exception as e:
			return False
