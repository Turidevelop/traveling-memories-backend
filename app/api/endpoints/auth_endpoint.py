from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.core.schemas import UserCreate, UserOut, Token
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserOut, status_code=201)
async def register(data: UserCreate, service: UserService = Depends()) -> UserOut:
    """Register a new user."""
    return await service.register(data)

@router.post("/login", response_model=Token)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(),
) -> Token:
    """Login and receive a JWT token. Use 'username' field for the name."""
    return await service.login(form.username, form.password)