from pydantic import BaseModel
import datetime
from typing import Optional

class CreateTaskPayload(BaseModel):
    name: str
    status: str | None
    due_date: datetime.datetime
    priority_level: str
    description: Optional[str] = None
    category: str

class UpdateTaskPayload(BaseModel):
    name: str | None
    description: str | None
    due_date: datetime.datetime | None
    category:str

class CreateUserPayload(BaseModel):
    name: str
    email: str
    mobile: str

class UpdateUserPayload(BaseModel):
    name: str | None = None
    email: str | None = None
    mobile: str | None = None


class UpdateTaskStatusPayload(BaseModel):
    status: str 


class CreateCategoryPayload(BaseModel):
    name: str

