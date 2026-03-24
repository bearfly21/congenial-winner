from pydantic import BaseModel
from typing import Optional


# --- Auth Schemas ---

class OTPRequest(BaseModel):
    phone: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class OTPVerify(BaseModel):
    phone: str
    code: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    phone: str
    first_name: str
    last_name: str
    xp: int
    level: int
    streak_days: int
    is_admin: bool

    model_config = {"from_attributes": True}
