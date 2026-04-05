from datetime import datetime

from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    note: str = ""


class TodoUpdate(BaseModel):
    title: str | None = None
    note: str | None = None
    done: bool | None = None


class TodoRead(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    title: str
    note: str
    done: bool
    created_at: datetime
