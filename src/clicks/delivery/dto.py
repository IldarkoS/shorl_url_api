from pydantic import BaseModel


class ClickStatsResponse(BaseModel):
    link: str
    original_link: str
    last_hour_clicks: int
    last_day_clicks: int
