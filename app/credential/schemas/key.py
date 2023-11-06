from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class KeyRequest(BaseModel):
	name: str
	developer: str

	class Config:
		orm_mode = True
