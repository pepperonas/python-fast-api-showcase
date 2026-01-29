"""Common DTOs (Data Transfer Objects) for microservices."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class BaseDTO(BaseModel):
    """Base DTO with common fields."""
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class UserDTO(BaseDTO):
    """User data transfer object."""
    id: str
    email: EmailStr
    full_name: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class TaskDTO(BaseDTO):
    """Task data transfer object."""
    id: str
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    project_id: Optional[str] = None
    assigned_to: Optional[str] = None
    created_by: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class ProjectDTO(BaseDTO):
    """Project data transfer object."""
    id: str
    name: str
    description: Optional[str] = None
    created_by: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class NotificationDTO(BaseDTO):
    """Notification data transfer object."""
    id: str
    user_id: str
    title: str
    message: str
    type: str
    read: bool
    created_at: datetime
