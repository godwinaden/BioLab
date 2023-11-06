from fastapi import APIRouter, Depends

from app.faces.repositories.face_repo import FaceRepo
from app.faces.schemas.face import FaceRequest
from app.faces.schemas.bio_response import BioCreateResponse, BioSearchResponse, BioSearchRequest

FaceRouter = APIRouter(
	prefix="/api/faces",
	tags=["Faces"],
	dependencies=[],
	responses={404: {"description": "Not Found"}, 201: {"description": "Successfully Executed"}},
)


@FaceRouter.post("/", response_model=BioCreateResponse, status_code=201)
def create(new_face: FaceRequest, repo: FaceRepo = Depends(FaceRepo)):
	return repo.create(new_face)


@FaceRouter.get("/{new_face_template}", response_model=BioSearchResponse, status_code=200)
def search(new_face_template: int, repo: FaceRepo = Depends(FaceRepo)):
	return repo.search(BioSearchRequest(template=new_face_template))
