from app.database.models.face_model import Face
from app.faces.schemas.face import FaceRequest
from app.faces.schemas.bio_response import BioCreateResponse, BioSearchResponse, BioSearchRequest
from fastapi.responses import JSONResponse
from starlette import status


class FaceRepo:

	@staticmethod
	def create(newFace: FaceRequest) -> JSONResponse | BioCreateResponse:
		try:
			return Face.create_face(newFace)
		except Exception as e:
			return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": f"Bad Request: {e}"})

	@staticmethod
	def search(alien_face: BioSearchRequest) -> JSONResponse | BioSearchResponse:
		try:
			return Face.search_face(alien_face)
		except Exception as e:
			return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": f"Bad Request: {e}"})
