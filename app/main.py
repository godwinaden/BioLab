from contextlib import asynccontextmanager
from fastapi import FastAPI
from cassandra.cqlengine.management import sync_table
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from app.config import get_settings, set_logger
from app.database import db
from app.credential.routers.credential_rest import API_CredentialRouter
from app.credential.routers.credential_gql import GQL_CredentialRouter
from app import exceptions
from app import handlers
from app.database.models.credential_model import ApiCredential
from app.database.models.face_model import Face
from app.database.models.finger_model import Finger
from app.database.models.user_model import User
from app.faces.routers.face_rest import FaceRouter
from app.fingers.routers.finger_rest import FingerRouter
from app.security import validate_public_key
from app.users.routers.user_rest import UserRouter

DB_SESSION = None
settings = get_settings()
settings.db_session = db.get_session()
set_logger()


@asynccontextmanager
async def lifespan():
	global DB_SESSION
	DB_SESSION = db.get_session()
	sync_table(Face)
	sync_table(Finger)
	sync_table(ApiCredential)
	sync_table(User)
	yield


app = FastAPI(
	lifespan=lifespan,
	title="BioLab  Server",
	description="Building Truly Secure Biometrics With AI Capabilities.",
	debug=True if settings.environment == "dev" else False,
	version="0.0.1",
	dependencies=[]
)

# app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_methods=["*"],
	allow_headers=["*"],
	allow_credentials=True,
)
app.add_exception_handler(exceptions.BioException, handlers.flight_exception_handler)
app.add_exception_handler(exceptions.CredentialsExistException, handlers.credential_exception_handler)
app.add_exception_handler(exceptions.CredentialsNotFoundException, handlers.no_credential_exception_handler)
app.add_exception_handler(exceptions.LoginRequiredException, handlers.login_needed_handler)

app.include_router(UserRouter)
app.include_router(FingerRouter)
app.include_router(FaceRouter)
app.include_router(API_CredentialRouter)
app.include_router(GQL_CredentialRouter)

if __name__ == "__main__":
	uvicorn.run("main:app", log_level="info", reload=True)
