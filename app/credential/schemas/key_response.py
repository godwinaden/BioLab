
from typing import Any
from pydantic import BaseModel

class KeyBase(BaseModel):
    app_key: Any
    app_name: str

class KeyResponse(KeyBase):
    public_key: str
    secret_key: str

class DeletedKeyResponse(KeyBase):
	pass
