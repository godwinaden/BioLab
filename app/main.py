from contextlib import asynccontextmanager
from fastapi import FastAPI
from cassandra.cqlengine.management import sync_table
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from app.config import get_settings, set_logger
from app.database import db
from app.database.models import api_calls, airport_city_code, api_credential
from app.flights.routers.flights_rest import API_FlightsRouter
from app.flights.routers.flights_gql import GQL_FlightsRouter
from app.insights.routers.insights_rest import API_InsightsRouter
from app.insights.routers.insights_gql import GQL_InsightsRouter
from app.itinerary.routers.itinerary_rest import API_ItineraryRouter
from app.itinerary.routers.itinerary_gql import GQL_ItineraryRouter
from app.credential.routers.credential_rest import API_CredentialRouter
from app.credential.routers.credential_gql import GQL_CredentialRouter
from app import exceptions
from app import handlers
from app.security import validate_public_key

DB_SESSION = None
settings = get_settings()
settings.db_session = db.get_session()
set_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(api_calls.AppCall)
    sync_table(airport_city_code.AirportCityCode)
    sync_table(api_credential.ApiCredential)
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
app.add_exception_handler(exceptions.FlightException, handlers.flight_exception_handler)
app.add_exception_handler(exceptions.CredentialsExistException, handlers.credential_exception_handler)
app.add_exception_handler(exceptions.CredentialsNotFoundException, handlers.no_credential_exception_handler)
app.add_exception_handler(exceptions.LoginRequiredException, handlers.login_needed_handler)

app.include_router(API_FlightsRouter)
app.include_router(GQL_FlightsRouter)
app.include_router(API_InsightsRouter)
app.include_router(GQL_InsightsRouter)
app.include_router(API_ItineraryRouter)
app.include_router(GQL_ItineraryRouter)
app.include_router(API_CredentialRouter)
app.include_router(GQL_CredentialRouter)

if __name__ == "__main__":
    uvicorn.run("main:app", log_level="info", reload=True)
