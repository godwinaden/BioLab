from fastapi import APIRouter, Depends

from app.faces.schemas.bio_response import BioCreateResponse, BioSearchResponse, BioSearchRequest
from app.fingers.repositories.finger_repo import FingerRepo
from app.fingers.schemas.finger_request import FingerRequest

FingerRouter = APIRouter(
	prefix="/api/fingers",
	tags=["Fingers"],
	dependencies=[],
	responses={404: {"description": "Not Found"}, 201: {"description": "Successfully Executed"}},
)


@FingerRouter.post("/", response_model=BioCreateResponse, status_code=201)
def create(new_finger: FingerRequest, repo: FingerRepo = Depends(FingerRepo)):
	return repo.create(new_finger)


@FingerRouter.get("/{new_finger_template}", response_model=BioSearchResponse, status_code=200)
def search(new_finger_template: int, repo: FingerRepo = Depends(FingerRepo)):
	return repo.search(BioSearchRequest(template=new_finger_template))
