from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints.user_endpoint import router as user_router
from app.api.endpoints.trip_endopoint import router as trip_router
from app.api.endpoints.trip_entry_endpoint import router as trip_entry_router
from app.api.endpoints.city_endpoint import router as city_router
from app.api.endpoints.country_endpoint import router as country_router
from app.api.endpoints.auth_endpoint import router as auth_router
from app.api.endpoints.place_visited_endpoint import router as place_visited_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

# ── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://traveling-memories.vercel.app","http://localhost:4200"],          # en producción cambia esto por tu dominio frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(trip_router)
app.include_router(trip_entry_router)
app.include_router(city_router)
app.include_router(country_router)
app.include_router(place_visited_router)

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a Travelling Memories!"}