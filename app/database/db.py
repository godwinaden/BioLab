import pathlib
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine import connection

from app.config import get_settings

BASE_DIR = pathlib.Path(__file__).resolve().parent

settings = get_settings()
connect_file = (
    "secure-connect-ihotfly.zip" if settings.space == "ihotfly" else "connect.zip"
)

ASTRADB_CONNECT_BUNDLE = BASE_DIR / "restricted" / connect_file

ASTRADB_CLIENT_ID = settings.db_client_id
ASTRADB_CLIENT_SECRET = settings.db_client_secret


def get_session():
    cloud_config = {"secure_connect_bundle": ASTRADB_CONNECT_BUNDLE}
    auth_provider = PlainTextAuthProvider(ASTRADB_CLIENT_ID, ASTRADB_CLIENT_SECRET)
    cluster = Cluster(
        control_connection_timeout=None,
        cloud=cloud_config,
        auth_provider=auth_provider,
        protocol_version=3,
    )
    session = cluster.connect()
    connection.register_connection(str(session), session=session)
    connection.set_default_connection(str(session))
    return session
