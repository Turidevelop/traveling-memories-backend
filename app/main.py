from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.endpoints.user_endpoint import router as user_router
from app.api.endpoints.trip_endopoint import router as trip_router
from app.api.endpoints.trip_entry_endpoint import router as trip_entry_router
from app.api.endpoints.city_endpoint import router as city_router
from app.api.endpoints.country_endpoint import router as country_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager para startup y shutdown"""
    # Startup - no init necesario, tablas ya creadas en Neon
    yield
    # Shutdown (si necesitas hacer algo al apagar)

app = FastAPI(lifespan=lifespan)

app.include_router(user_router)

app.include_router(trip_router)

app.include_router(trip_entry_router)

app.include_router(city_router)

app.include_router(country_router)

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a Travelling Memories!"}


