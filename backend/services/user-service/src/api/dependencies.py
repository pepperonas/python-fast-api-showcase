"""FastAPI dependencies."""

import sys
from pathlib import Path

# Add backend directory to Python path for imports
backend_dir = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(backend_dir))

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from shared.database import get_db
from shared.auth import decode_access_token
from shared.dto import UserDTO
from src.infrastructure.repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UserDTO:
    """Get current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    repository = UserRepository(db)
    user = await repository.get_by_id(user_id)
    if user is None:
        raise credentials_exception
    
    return UserDTO(
        id=user.id,
        email=user.email.value,
        full_name=user.full_name,
        created_at=user.created_at,
        updated_at=user.updated_at
    )
