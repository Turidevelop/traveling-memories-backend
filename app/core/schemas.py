from datetime import date, datetime
from pydantic import BaseModel, field_validator


class UserOut(BaseModel):
    id: int
    name: str
    avatar_url: str | None = None
    bio: str | None = None
    model_config = {"from_attributes": True}


class UserCreate(BaseModel):
    name: str
    password: str
    avatar_url: str | None = None
    bio: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: int | None = None


class TripCreate(BaseModel):
    title: str
    start_date: date | None = None
    end_date: date | None = None
    user_id: int
    cover_photo_url: str | None = None
    summary: str | None = None
    is_wishlist: bool = False


class TripOut(TripCreate):
    id: int
    created_at: datetime | None = None
    model_config = {"from_attributes": True}


class TripEntryCreate(BaseModel):
    trip_id: int
    title: str | None = None
    entry_date: date | None = None
    text_trip: str | None = None
    photo_urls: list[str] = []

    @field_validator("photo_urls")
    @classmethod
    def max_five_photos(cls, v):
        if v and len(v) > 5:
            raise ValueError("Maximum 5 photos allowed per entry")
        return v


class TripEntryOut(TripEntryCreate):
    id: int
    created_at: datetime | None = None
    model_config = {"from_attributes": True}


class CityCreate(BaseModel):
    name: str
    lat: float
    lng: float
    country_id: int


class CityOut(CityCreate):
    id: int
    model_config = {"from_attributes": True}


class CountryCreate(BaseModel):
    name: str
    region: str | None = None
    lat: float | None = None
    lng: float | None = None


class CountryOut(CountryCreate):
    id: int
    model_config = {"from_attributes": True}


class PlaceVisitedCreate(BaseModel):
    trip_id: int
    country_id: int | None = None
    city_id: int | None = None

class PlaceVisitedOut(PlaceVisitedCreate):
    id: int
    model_config = {"from_attributes": True}