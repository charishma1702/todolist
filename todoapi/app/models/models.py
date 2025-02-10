from pydantic import BaseModel
import datetime
class CreateTaskPayload(BaseModel):
    name: str
    description: str | None
    status: str | None
    user_id: str
    due_date: datetime.datetime
    priority_level: int

class UpdateTaskPayload(BaseModel):
    name: str | None
    description: str | None
    status: str | None
    due_date: datetime.datetime | None


class CreateUserPayload(BaseModel):
    name: str
    email: str
    mobile: str

class UpdateUserPayload(BaseModel):
    name: str | None = None
    email: str | None = None
    mobile: str | None = None