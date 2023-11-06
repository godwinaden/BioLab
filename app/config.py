from datetime import datetime
import logging
import os
from pathlib import Path
from functools import lru_cache
import pathlib
from pydantic import BaseSettings, Field
from dotenv import load_dotenv
from amadeus import Client
from cassandra.cluster import Session

# Load environment variables from .env file
load_dotenv()

os.environ["CQLENG_ALLOW_SCHEMA_MANAGEMENT"] = "1"
app_environ: str = os.environ["ENVIRONMENT"]
app_space: str = os.environ["SPACE"]


def get_amadeus():
    id: str = os.environ["AMADEUS_TEST_KEY"]
    secret: str = os.environ["AMADEUS_TEST_SECRET"]
    if app_environ == "production":
        if app_space == "switz":
            id = os.environ["SWITZ_AMADEUS_PRODUCTION_KEY"]
            secret = os.environ["SWITZ_AMADEUS_PRODUCTION_SECRET"]
        else:
            id = os.environ["AMADEUS_PRODUCTION_KEY"]
            secret = os.environ["AMADEUS_PRODUCTION_SECRET"]
    else:
        if app_space == "switz":
            id = os.environ["SWITZ_AMADEUS_TEST_KEY"]
            secret = os.environ["SWITZ_AMADEUS_TEST_SECRET"]
    return id, secret


def get_astras():
    if app_space == "switz":
        astra_key = Field(..., env="SWITZ_ASTRADB_CLIENT_ID")
        astra_secret = Field(..., env="SWITZ_ASTRADB_CLIENT_SECRET")
        astra_token = Field(..., env="SWITZ_ASTRADB_APP_TOKEN")
        astra_store = Field(..., env="SWITZ_ASTRADB_KEYSPACE")
    else:
        astra_key = Field(..., env="ASTRADB_CLIENT_ID")
        astra_secret = Field(..., env="ASTRADB_CLIENT_SECRET")
        astra_token = Field(..., env="ASTRADB_APP_TOKEN")
        astra_store = Field(..., env="ASTRADB_KEYSPACE")
    return astra_key, astra_secret, astra_token, astra_store


id, secret = get_amadeus()
astra_key, astra_secret, astra_token, astra_store = get_astras()
amadeus = Client(
    client_id=id,
    client_secret=secret,
    hostname="production" if app_environ == "production" else "test",
)


class Settings(BaseSettings):
    base_dir: Path = Path(__file__).resolve().parent
    keyspace: str = astra_store
    db_client_id: str = astra_key
    db_client_secret: str = astra_secret
    db_client_token: str = astra_token
    environment: str = app_environ
    space: str = app_space
    amadeus: Client = amadeus
    logger: logging.Logger | logging.RootLogger = logging.getLogger()
    log_file: str = ""
    db_session: Session = None

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()


@lru_cache
def set_logger():
	file_name = datetime.now().strftime("%d-%m-%Y.log")
	BASE_DIR = pathlib.Path(__file__).resolve().parent
	LOG_PATH = BASE_DIR / "logs" / file_name
	settings = get_settings()
	settings.logger.setLevel(logging.DEBUG)

	# create file handler which logs even debug messages
	fh = logging.FileHandler(LOG_PATH)
	fh.setLevel(logging.DEBUG)

	# create console handler with a higher log level
	sh = logging.StreamHandler()
	sh.setLevel(logging.ERROR)

	# create formatter and add it to the handlers
	formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
	sh.setFormatter(formatter)
	fh.setFormatter(formatter)

	# add the handlers to logger
	settings.logger.addHandler(sh)
	settings.logger.addHandler(fh)
	settings.log_file = LOG_PATH
