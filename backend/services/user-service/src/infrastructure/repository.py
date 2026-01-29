"""User repository implementation (infrastructure layer)."""

from typing import Optional
from sqlalchemy.orm import Session
from src.domain.user import User
from src.domain.value_objects import Email
from src.domain.repository import IUserRepository
from src.infrastructure.models import UserModel


class UserRepository(IUserRepository):
    """SQLAlchemy implementation of user repository."""
    
    def __init__(self, db: Session):
        self._db = db
    
    async def create(self, user: User) -> User:
        """Create a new user."""
        db_user = UserModel(
            id=user.id,
            email=user.email.value,
            full_name=user.full_name,
            password_hash=user.password_hash,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        self._db.add(db_user)
        self._db.commit()
        self._db.refresh(db_user)
        return self._to_domain(db_user)
    
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        db_user = self._db.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_domain(db_user) if db_user else None
    
    async def get_by_email(self, email: Email) -> Optional[User]:
        """Get user by email."""
        db_user = self._db.query(UserModel).filter(UserModel.email == email.value).first()
        return self._to_domain(db_user) if db_user else None
    
    async def update(self, user: User) -> User:
        """Update an existing user."""
        db_user = self._db.query(UserModel).filter(UserModel.id == user.id).first()
        if not db_user:
            raise ValueError(f"User with id {user.id} not found")
        
        db_user.full_name = user.full_name
        db_user.updated_at = user.updated_at
        self._db.commit()
        self._db.refresh(db_user)
        return self._to_domain(db_user)
    
    def _to_domain(self, db_user: UserModel) -> User:
        """Convert database model to domain entity."""
        return User(
            user_id=db_user.id,
            email=Email(db_user.email),
            full_name=db_user.full_name,
            password_hash=db_user.password_hash,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )
