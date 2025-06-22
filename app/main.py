from fastapi import FastAPI
from app.api.endpoints.health_endpoint import router as health_router



app = FastAPI()

app.include_router(health_router)


@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a Travelling Memories!"}


