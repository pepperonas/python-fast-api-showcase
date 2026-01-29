"""Notification domain entity."""

from datetime import datetime
from typing import Optional
from uuid import uuid4
from enum import Enum


class NotificationType(str, Enum):
    """Notification type value object."""
    TASK_ASSIGNED = "task_assigned"
    TASK_UPDATED = "task_updated"
    TASK_COMPLETED = "task_completed"
    PROJECT_CREATED = "project_created"


class Notification:
    """Notification domain entity following DDD principles."""
    
    def __init__(
        self,
        user_id: str,
        title: str,
        message: str,
        notification_type: NotificationType,
        notification_id: Optional[str] = None,
        read: bool = False,
        created_at: Optional[datetime] = None
    ):
        if not title or len(title.strip()) == 0:
            raise ValueError("Notification title cannot be empty")
        if not message or len(message.strip()) == 0:
            raise ValueError("Notification message cannot be empty")
        
        self._id = notification_id or str(uuid4())
        self._user_id = user_id
        self._title = title.strip()
        self._message = message.strip()
        self._type = notification_type
        self._read = read
        self._created_at = created_at or datetime.utcnow()
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def user_id(self) -> str:
        return self._user_id
    
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def message(self) -> str:
        return self._message
    
    @property
    def type(self) -> NotificationType:
        return self._type
    
    @property
    def read(self) -> bool:
        return self._read
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    def mark_as_read(self) -> None:
        """Mark notification as read."""
        self._read = True
    
    def mark_as_unread(self) -> None:
        """Mark notification as unread."""
        self._read = False
