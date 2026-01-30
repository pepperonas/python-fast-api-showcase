"""FastAPI routes for user service."""

import sys
from pathlib import Path

# Add backend directory to Python path for imports
backend_dir = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(backend_dir))

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from shared.database import get_db
from shared.dto import UserDTO
from src.application.use_cases import (
    RegisterUserUseCase,
    AuthenticateUserUseCase,
    GetUserProfileUseCase
)
from src.infrastructure.repository import UserRepository
from src.api.dependencies import get_current_user

router = APIRouter(prefix="/api/v1", tags=["users"])


class RegisterRequest(BaseModel):
    """Request model for user registration."""
    email: EmailStr
    full_name: str
    password: str


class LoginRequest(BaseModel):
    """Request model for user login."""
    email: EmailStr
    password: str


@router.post("/auth/register", response_model=UserDTO, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    """Register a new user."""
    repository = UserRepository(db)
    use_case = RegisterUserUseCase(repository)
    
    try:
        user = await use_case.execute(
            email=request.email,
            full_name=request.full_name,
            password=request.password
        )
        return UserDTO(
            id=user.id,
            email=user.email.value,
            full_name=user.full_name,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/auth/login")
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """Authenticate user and get access token."""
    repository = UserRepository(db)
    use_case = AuthenticateUserUseCase(repository)
    
    result = await use_case.execute(
        email=request.email,
        password=request.password
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return result


@router.get("/users/me", response_model=UserDTO)
async def get_me(
    current_user: UserDTO = Depends(get_current_user)
):
    """Get current user profile."""
    return current_user


@router.get("/credentials")
async def get_credentials():
    """
    Dummy endpoint for browser extensions (password managers).
    Returns 404 to indicate this endpoint is not used.
    """
    from fastapi import HTTPException, status
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="This endpoint is not implemented. Use /api/v1/auth/login for authentication."
    )


@router.get("/users/{user_id}", response_model=UserDTO)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: UserDTO = Depends(get_current_user)
):
    """Get user profile by ID."""
    repository = UserRepository(db)
    use_case = GetUserProfileUseCase(repository)
    
    user = await use_case.execute(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserDTO(
        id=user.id,
        email=user.email.value,
        full_name=user.full_name,
        created_at=user.created_at,
        updated_at=user.updated_at
    )
