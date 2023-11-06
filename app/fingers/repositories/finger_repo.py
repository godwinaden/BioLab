from app.database.models.finger_model import Finger
from app.faces.schemas.bio_response import BioCreateResponse, BioSearchResponse, BioSearchRequest
from fastapi.responses import JSONResponse
from starlette import status

from app.fingers.schemas.finger_request import FingerRequest


class FingerRepo:

	@staticmethod
	def create(newFinger: FingerRequest) -> JSONResponse | BioCreateResponse:
		try:
			return Finger.create_face(newFinger)
		except Exception as e:
			return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": f"Bad Request: {e}"})

	@staticmethod
	def search(alien_face: BioSearchRequest) -> JSONResponse | BioSearchResponse:
		try:
			return Finger.search_face(alien_face)
		except Exception as e:
			return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": f"Bad Request: {e}"})
