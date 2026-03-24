from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import OTPRequest, OTPVerify, TokenResponse, UserResponse
from app.services.otp import send_otp, verify_otp
from app.utils.security import create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/send-otp")
def send_otp_endpoint(data: OTPRequest, db: Session = Depends(get_db)):
    """Send OTP to phone number. Creates user if not exists."""
    user = db.query(User).filter(User.phone == data.phone).first()

    if user is None:
        # First time → require name
        if not data.first_name or not data.last_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="first_name and last_name required for new users",
            )
        user = User(
            phone=data.phone,
            first_name=data.first_name,
            last_name=data.last_name,
        )
        db.add(user)
        db.commit()

    code = send_otp(data.phone)
    return {"message": f"OTP sent to {data.phone}", "debug_code": code}


@router.post("/verify-otp", response_model=TokenResponse)
def verify_otp_endpoint(data: OTPVerify, db: Session = Depends(get_db)):
    """Verify OTP and return JWT token."""
    if not verify_otp(data.phone, data.code):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid OTP code",
        )

    user = db.query(User).filter(User.phone == data.phone).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found. Send OTP first.",
        )

    token = create_access_token(user.id)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get current user profile."""
    return current_user
