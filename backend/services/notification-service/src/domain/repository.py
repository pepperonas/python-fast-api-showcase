"""Notification repository interface (domain layer)."""

from abc import ABC, abstractmethod
from typing import Optional, List
from .notification import Notification


class INotificationRepository(ABC):
    """Interface for notification repository."""
    
    @abstractmethod
    async def create(self, notification: Notification) -> Notification:
        """Create a new notification."""
        pass
    
    @abstractmethod
    async def get_by_id(self, notification_id: str) -> Optional[Notification]:
        """Get notification by ID."""
        pass
    
    @abstractmethod
    async def get_by_user(self, user_id: str, unread_only: bool = False) -> List[Notification]:
        """Get notifications for a user."""
        pass
    
    @abstractmethod
    async def update(self, notification: Notification) -> Notification:
        """Update an existing notification."""
        pass
    
    @abstractmethod
    async def mark_all_as_read(self, user_id: str) -> int:
        """Mark all notifications as read for a user."""
        pass
