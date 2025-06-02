from datetime import datetime

from pydantic import BaseModel, HttpUrl, Field, AnyHttpUrl


class CreateShortURLRequest(BaseModel):
    original_url: HttpUrl
    expires_at: datetime | None = None


class CreateShortURLResponse(BaseModel):
    url: AnyHttpUrl


class ShortURLResponse(BaseModel):
    id: int
    code: str
    original_url: HttpUrl
    is_active: bool
    created_at: datetime
    expires_at: datetime


class FilterParamsShortURLsRequest(BaseModel):
    is_active: bool | None = Field(None)
    offset: int = Field(0)
    limit: int = Field(20)
