from fastapi import FastAPI
from app.api.endpoints.user_endpoint import router as user_router
from app.api.endpoints.trip_endopoint import router as trip_router
from app.api.endpoints.place_visited_endpoint import router as place_visited_router
from app.api.endpoints.trip_entry_endpoint import router as trip_entry_router
from app.api.endpoints.city_endpoint import router as city_router
from app.api.endpoints.country_endpoint import router as country_router

app = FastAPI()

app.include_router(user_router)

app.include_router(trip_router)

app.include_router(place_visited_router)

app.include_router(trip_entry_router)

app.include_router(city_router)

app.include_router(country_router)

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a Travelling Memories!"}


