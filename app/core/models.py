from datetime import datetime, date

from sqlalchemy import Integer, Float, String, Text, Date, ForeignKey, TIMESTAMP, Boolean, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "appuser"
    __table_args__ = {"schema": "travel"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)


class Trip(Base):
    __tablename__ = "trip"
    __table_args__ = {"schema": "travel"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("travel.appuser.id"), nullable=False)
    cover_photo_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_wishlist: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), nullable=False
    )


class TripEntry(Base):
    __tablename__ = "trip_entry"
    __table_args__ = {"schema": "travel"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    trip_id: Mapped[int] = mapped_column(Integer, ForeignKey("travel.trip.id"), nullable=True)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    entry_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    text_trip: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), nullable=False
    )
    photo_urls: Mapped[list[str]] = mapped_column(ARRAY(Text), default=list, nullable=False)


class City(Base):
    __tablename__ = "city"
    __table_args__ = {"schema": "travel"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    lat: Mapped[float] = mapped_column(Float, nullable=False)
    lng: Mapped[float] = mapped_column(Float, nullable=False)
    country_id: Mapped[int] = mapped_column(Integer, ForeignKey("travel.country.id"), nullable=False)


class Country(Base):
    __tablename__ = "country"
    __table_args__ = {"schema": "travel"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    region: Mapped[str | None] = mapped_column(String(100), nullable=True)
    lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    lng: Mapped[float | None] = mapped_column(Float, nullable=True)


class PlaceVisited(Base):
    __tablename__ = "place_visited"
    __table_args__ = {"schema": "travel"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    trip_id: Mapped[int] = mapped_column(Integer, ForeignKey("travel.trip.id", ondelete="CASCADE"), nullable=False)
    country_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("travel.country.id"), nullable=True)
    city_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("travel.city.id"), nullable=True)