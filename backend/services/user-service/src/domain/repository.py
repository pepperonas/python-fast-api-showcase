"""User repository interface (domain layer)."""

from abc import ABC, abstractmethod
from typing import Optional
from .user import User
from .value_objects import Email


class IUserRepository(ABC):
    """Interface for user repository following Repository pattern."""
    
    @abstractmethod
    async def create(self, user: User) -> User:
        """Create a new user."""
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: Email) -> Optional[User]:
        """Get user by email."""
        pass
    
    @abstractmethod
    async def update(self, user: User) -> User:
        """Update an existing user."""
        pass
