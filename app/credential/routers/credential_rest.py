from typing import List
from fastapi import APIRouter, Depends, Request
from fastapi.security.api_key import APIKey as FastApiKey
from app.security import validate_public_key
from app.credential.schemas.key_response import DeletedKeyResponse, KeyResponse
from app.credential.schemas.key import KeyRequest
from app.credential.repositories.key_repo import KeyRepo

API_CredentialRouter = APIRouter(
	prefix="/api/credentials",
	tags=["Credentials"],
	dependencies=[],
	responses={404: {"description": "Not Found"}, 201: {"description": "Successfully Executed"}},
)


@API_CredentialRouter.get("/", status_code=200, response_model=List[KeyResponse])
def get_all(request: Request, repo: KeyRepo = Depends(KeyRepo), api_key: FastApiKey = Depends(validate_public_key)):
	return repo.get_all_credentials(request, api_key)


@API_CredentialRouter.get("/{app_name}", response_model=KeyResponse, status_code=200)
def get_mine(request: Request, app_name: str, repo: KeyRepo = Depends(KeyRepo), api_key: FastApiKey = Depends(validate_public_key)):
	return repo.get_credentials(request, app_name, api_key)


@API_CredentialRouter.post("/create", response_model=KeyResponse, status_code=201)
def create(request: Request, credentials: KeyRequest, repo: KeyRepo = Depends(KeyRepo)):
	return repo.create_credentials(request, credentials)


@API_CredentialRouter.delete("/delete/{app_name}", response_model=DeletedKeyResponse, status_code=201)
def delete(request: Request, app_name: str, repo: KeyRepo = Depends(KeyRepo), api_key: FastApiKey = Depends(validate_public_key)):
	return repo.delete_credentials(request, app_name, api_key)
