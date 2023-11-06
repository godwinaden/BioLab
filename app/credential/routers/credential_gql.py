from fastapi import APIRouter, Depends
from app.security import validate_public_key


GQL_CredentialRouter = APIRouter(
    prefix="/gql/credentials",
    tags=["Credentials"],
    dependencies=[Depends(validate_public_key)],
    responses={404: {"description": "Not found"}},
)


@GQL_CredentialRouter.get("/")
def all():
    pass
