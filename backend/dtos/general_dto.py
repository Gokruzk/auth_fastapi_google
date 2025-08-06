from enum import Enum
from pydantic import BaseModel
from typing import Optional, TypeVar

T = TypeVar("T")


class BaseDTO(BaseModel):

    class Config:
        from_attributes = True


class ResponseSchema(BaseDTO):
    detail: str
    result: Optional[T] = None


class Role(str, Enum):
    admin = "Admin"
    user = "User"
