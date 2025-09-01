from fastapi import FastAPI
from app.api.endpoints.users_endpoint import router as users_router
from app.api.endpoints.trip_endopoint import router as trip_router
from app.api.endpoints.place_visited_endpoint import router as place_visited_router
app = FastAPI()

app.include_router(users_router)

app.include_router(trip_router)

app.include_router(place_visited_router)

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a Travelling Memories!"}


