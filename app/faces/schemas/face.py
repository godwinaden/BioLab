from datetime import datetime

from pydantic import BaseModel


class FaceRequest(BaseModel):
	user_id: str
	template: int
	created_on: datetime

	class Config:
		orm_mode = True

