"""Use cases for user service (application layer)."""

import sys
from pathlib import Path

# Add backend directory to Python path for imports
backend_dir = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(backend_dir))

from typing import Optional
from datetime import timedelta
from shared.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from src.domain.user import User
from src.domain.value_objects import Email, Password
from src.domain.repository import IUserRepository


class RegisterUserUseCase:
    """Use case for registering a new user."""
    
    def __init__(self, user_repository: IUserRepository):
        self._user_repository = user_repository
    
    async def execute(
        self,
        email: str,
        full_name: str,
        password: str
    ) -> User:
        """Register a new user."""
        # Check if user already exists
        email_vo = Email(email)
        existing_user = await self._user_repository.get_by_email(email_vo)
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Create new user
        password_hash = get_password_hash(password)
        user = User(
            email=email_vo,
            full_name=full_name,
            password_hash=password_hash
        )
        
        return await self._user_repository.create(user)


class AuthenticateUserUseCase:
    """Use case for authenticating a user."""
    
    def __init__(self, user_repository: IUserRepository):
        self._user_repository = user_repository
    
    async def execute(
        self,
        email: str,
        password: str
    ) -> Optional[dict]:
        """Authenticate user and return access token."""
        email_vo = Email(email)
        user = await self._user_repository.get_by_email(email_vo)
        
        if not user:
            return None
        
        password_vo = Password(password)
        if not user.verify_password(password_vo, verify_password):
            return None
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.id, "email": user.email.value},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email.value,
                "full_name": user.full_name
            }
        }


class GetUserProfileUseCase:
    """Use case for getting user profile."""
    
    def __init__(self, user_repository: IUserRepository):
        self._user_repository = user_repository
    
    async def execute(self, user_id: str) -> Optional[User]:
        """Get user profile by ID."""
        return await self._user_repository.get_by_id(user_id)
