# api/dependencies.py
from database import get_db
from core.config import settings

def get_db_session():
    return next(get_db())

def is_production():
    return settings.ENVIRONMENT == "production"