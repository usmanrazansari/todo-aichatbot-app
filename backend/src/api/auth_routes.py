from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from src.utils.jwt_handler import create_access_token
from datetime import timedelta

router = APIRouter()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    email: str


@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    """
    Demo login endpoint - accepts any email/password combination.
    In production, this would validate against a user database.
    """
    # Generate user ID from email
    user_id = f"user_{request.email.split('@')[0]}_{hash(request.email) % 100000}"

    # Create JWT token with user info
    token_data = {
        "user_id": user_id,
        "email": request.email
    }
    access_token = create_access_token(
        data=token_data,
        expires_delta=timedelta(days=1)
    )

    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user_id,
        email=request.email
    )


@router.post("/register", response_model=AuthResponse)
async def register(request: RegisterRequest):
    """
    Demo register endpoint - accepts any email/password combination.
    In production, this would create a user in the database.
    """
    # Validate password length
    if len(request.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters long"
        )

    # Generate user ID from email
    user_id = f"user_{request.email.split('@')[0]}_{hash(request.email) % 100000}"

    # Create JWT token with user info
    token_data = {
        "user_id": user_id,
        "email": request.email
    }
    access_token = create_access_token(
        data=token_data,
        expires_delta=timedelta(days=1)
    )

    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user_id,
        email=request.email
    )
