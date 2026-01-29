"""User domain entity."""

from datetime import datetime
from typing import Optional
from uuid import uuid4
from .value_objects import Email, Password


class User:
    """User domain entity following DDD principles."""
    
    def __init__(
        self,
        email: Email,
        full_name: str,
        password_hash: str,
        user_id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self._id = user_id or str(uuid4())
        self._email = email
        self._full_name = full_name
        self._password_hash = password_hash
        self._created_at = created_at or datetime.utcnow()
        self._updated_at = updated_at
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def email(self) -> Email:
        return self._email
    
    @property
    def full_name(self) -> str:
        return self._full_name
    
    @property
    def password_hash(self) -> str:
        return self._password_hash
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def updated_at(self) -> Optional[datetime]:
        return self._updated_at
    
    def update_full_name(self, new_name: str) -> None:
        """Update user's full name."""
        if not new_name or len(new_name.strip()) == 0:
            raise ValueError("Full name cannot be empty")
        self._full_name = new_name.strip()
        self._updated_at = datetime.utcnow()
    
    def verify_password(self, password: Password, verify_func) -> bool:
        """Verify password against hash."""
        return verify_func(password.value, self._password_hash)
