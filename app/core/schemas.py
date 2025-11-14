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


class TripEntryCreate(BaseModel):
    trip_id: int
    entry_date: date
    title: str
    content: str

class TripEntryOut(TripEntryCreate):
    id: int

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

class CountryOut(CountryCreate):
    id: int
    model_config = {"from_attributes": True}