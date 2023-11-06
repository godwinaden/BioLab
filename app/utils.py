import json
import time
from typing import Optional

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from pydantic import BaseModel, error_wrappers
from app.config import get_settings

durations: list = []
settings = get_settings()


def valid_schema_data_or_error(raw_data: dict, SchemaModel: BaseModel):
	"""

	@param raw_data:
	@type SchemaModel: BaseModel
	"""
	data = {}
	errors = []
	error_str = None
	try:
		cleaned_data = SchemaModel(**raw_data)
		data = cleaned_data.dict()
	except error_wrappers.ValidationError as e:
		error_str = e.json()
	if error_str is not None:
		try:
			errors = json.loads(error_str)
		except Exception as e:
			errors = [{"loc": "non_field_error", "msg": "Unknown error"}]
			print(e)
	return data, errors


def timed(func):
	def wrapper(*args, **kwargs):
		start = time.perf_counter()
		log(msg="{name:<30} started".format(name=func.__name__), level=20)
		result = func(*args, **kwargs)
		duration = "{name:<30} finished in {elapsed:.2f} seconds".format(
			name=func.__name__, elapsed=time.perf_counter() - start
		)
		log(msg=duration, level=20)
		durations.append(duration)
		return result

	return wrapper


"""_summary_
	the message type desc:
	10 => debug | 20 => info | 30 => warning | 40 => error | 50 => critical
"""


def log(msg: str, level: int = 20, exc: Optional[Exception] = None):
	settings.logger.log(level=level, msg=msg, exc_info=exc)


def db_transact(query: str):
	db = settings.db_session
	set_keyspace = db.execute("USE " + settings.keyspace)
	if set_keyspace is not None:
		return db.execute(query)
	else:
		return None


def generate_hash(credl_raw):
	ph = PasswordHasher()
	return ph.hash(credl_raw)


def verify_hash(credl_hashed, credl_raw):
	ph = PasswordHasher()
	verified = False
	msg = "verified Successfully."
	try:
		verified = ph.verify(credl_hashed, credl_raw)
	except VerifyMismatchError as v:
		verified = False
		msg = f"Invalid Credential. {repr(v)}"
	except Exception as e:
		verified = False
		msg = f"Unexpected Error: \n{e}"
	return verified, msg
