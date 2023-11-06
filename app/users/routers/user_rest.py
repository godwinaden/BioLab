from fastapi import APIRouter, Depends

from app.faces.schemas.bio_response import BioCreateResponse, BioSearchResponse, BioSearchRequest
from app.users.repositories.user_repo import UserRepo
from app.users.schemas.user_request import UserRequest

UserRouter = APIRouter(
	prefix="/api/users",
	tags=["Users"],
	dependencies=[],
	responses={404: {"description": "Not Found"}, 201: {"description": "Successfully Executed"}},
)


@UserRouter.post("/", response_model=BioCreateResponse, status_code=201)
def create(new_user: UserRequest, repo: UserRepo = Depends(UserRepo)):
	return repo.create(new_user)


@UserRouter.get("/{user_id}", response_model=UserRequest, status_code=200)
def get_user(user_id: str, repo: UserRepo = Depends(UserRepo)):
	return repo.get_user(user_id)
