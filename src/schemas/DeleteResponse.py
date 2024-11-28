import uuid

from pydantic import BaseModel


class DeleteResponse(BaseModel):
    id: uuid.UUID
    message: str
    status: str
