from typing import Optional

from pydantic import BaseModel, Field


class BaseField(BaseModel):
    password: Optional[str]


class AddPaste(BaseField):
    text: str = Field(...)


class GetPaste(BaseField):
    id: str = Field(...)
