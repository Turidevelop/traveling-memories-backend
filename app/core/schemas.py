from datetime import date, datetime
from pydantic import BaseModel

class UserOut(BaseModel):
    id: int
    name: str
    avatar_url: str | None = None
    bio: str | None = None

    model_config = {"from_attributes": True}



class TripCreate(BaseModel):
    title: str
    start_date: date | None = None
    end_date: date | None = None
    user_id: int
    cover_photo_url: str | None = None
    summary: str | None = None

class TripOut(TripCreate):
    id: int
    created_at: datetime | None = None

    model_config = {"from_attributes": True}

class PlaceVisitedCreate(BaseModel):
    trip_id: int
    country_id: int
    city_id: int

class PlaceVisitedOut(PlaceVisitedCreate):
    id: int

    model_config = {"from_attributes": True}