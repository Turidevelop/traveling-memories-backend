from fastapi import FastAPI
from app.api.endpoints.users_endpoint import router as users_router
from app.api.endpoints.trip_endopoint import router as trip_router

app = FastAPI()

app.include_router(users_router)

app.include_router(trip_router)

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a Travelling Memories!"}


