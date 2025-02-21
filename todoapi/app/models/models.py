from pydantic import BaseModel, EmailStr
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
    priority_level:str | None

class CreateUserPayload(BaseModel):
    name: str
    email: EmailStr
    password: str

class UpdateUserPayload(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None

class LoginRequest(BaseModel):
    email:EmailStr
    password:str

class UpdateTaskStatusPayload(BaseModel):
    status: str 


class CreateCategoryPayload(BaseModel):
    name: str


class UpdateCategoryPayload(BaseModel):
    name: str | None = None
    

