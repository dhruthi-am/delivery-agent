from pydantic import BaseModel

class CallRequest(BaseModel):
    message: str