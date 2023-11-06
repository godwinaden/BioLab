from datetime import datetime

from pydantic import BaseModel


class FingerRequest(BaseModel):
	type: str
	category: str
	user_id: str
	template: int
	created_on: datetime

	class Config:
		orm_mode = True

