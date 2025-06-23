from pydantic import BaseModel

class AppUser(BaseModel):
    id: int
    name: str
    avatar_url: str | None = None
    bio: str | None = None

    model_config = {"from_attributes": True}
