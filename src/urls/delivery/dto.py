from datetime import datetime

from pydantic import BaseModel, HttpUrl, Field, AnyHttpUrl

from src.urls.domain.entity import URL


class CreateShortURLRequest(BaseModel):
    original_url: HttpUrl
    expires_at: datetime | None = None

    def to_entity(self, user_id: int):
        return URL(
            original_url=str(self.original_url),
            expires_at=self.expires_at,
            user_id=user_id,
        )


class CreateShortURLResponse(BaseModel):
    url: AnyHttpUrl


class ShortURLResponse(BaseModel):
    id: int
    code: str
    original_url: HttpUrl
    is_active: bool
    created_at: datetime
    expires_at: datetime

    @classmethod
    def from_entity(cls, entity: URL):
        return cls(
            id=entity.id,
            code=entity.code,
            original_url=entity.original_url,
            is_active=entity.is_active,
            expires_at=entity.expires_at,
            created_at=entity.created_at,
        )


class FilterParamsShortURLsRequest(BaseModel):
    is_active: bool | None = Field(None)
    offset: int = Field(0)
    limit: int = Field(20)
