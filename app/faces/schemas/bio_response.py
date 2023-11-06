from datetime import datetime

from pydantic import BaseModel


class BioSearchRequest(BaseModel):
	template: int

	class Config:
		orm_mode = True


class BioSearchResponse(BaseModel):
	accuracy: float
	description: str
	search_algorithm: str

	class Config:
		orm_mode = True


class BioCreateResponse(BaseModel):
	saved: bool
	time_saved: datetime

	class Config:
		orm_mode = True
