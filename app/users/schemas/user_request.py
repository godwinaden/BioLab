from datetime import datetime

from pydantic import BaseModel


class UserRequest(BaseModel):
	id_type: str
	id_type_number: str
	gender: str
	state: str
	location: str
	full_name: str
	marital_status: str
	created_on: datetime

	class Config:
		orm_mode = True

