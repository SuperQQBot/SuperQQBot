from pydantic import BaseModel
from typing import Optional

class ValidationRequest(BaseModel):
    plain_token: str

class ValidationResponse(BaseModel):
    plain_token: str
    signature: str

def serialize_response(response_obj):
    return response_obj.json()
