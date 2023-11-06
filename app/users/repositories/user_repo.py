from app.database.models.user_model import User
from app.faces.schemas.bio_response import BioCreateResponse, BioSearchResponse, BioSearchRequest
from fastapi.responses import JSONResponse
from starlette import status

from app.users.schemas.user_request import UserRequest


class UserRepo:

	@staticmethod
	def create(newFinger: UserRequest) -> JSONResponse | BioCreateResponse:
		try:
			return User.create_user(newFinger)
		except Exception as e:
			return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": f"Bad Request: {e}"})

	@staticmethod
	def get_user(user_id: str) -> JSONResponse | UserRequest:
		try:
			return User.get_user(user_id)
		except Exception as e:
			return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": f"Bad Request: {e}"})
