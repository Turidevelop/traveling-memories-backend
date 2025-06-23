from fastapi import FastAPI
from app.api.endpoints.health_endpoint import router as health_router
from app.api.endpoints.users_endpoint import router as users_router


app = FastAPI()

app.include_router(health_router)
app.include_router(users_router)

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a Travelling Memories!"}


