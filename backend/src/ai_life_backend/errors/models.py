# backend/src/ai_life_backend/errors/models.py
from pydantic import BaseModel, AnyUrl
from typing import Optional


class Problem(BaseModel):
    type: Optional[AnyUrl] = None
    title: str
    status: int
    detail: Optional[str] = None
    instance: Optional[AnyUrl] = None

    class Config:
        extra = "allow"  # позволяем доп.поля по RFC 7807/9457
