"""Use cases for notification service (application layer)."""

from typing import List
from src.domain.notification import Notification, NotificationType
from src.domain.repository import INotificationRepository


class SendNotificationUseCase:
    """Use case for sending a notification."""
    
    def __init__(self, notification_repository: INotificationRepository):
        self._notification_repository = notification_repository
    
    async def execute(
        self,
        user_id: str,
        title: str,
        message: str,
        notification_type: NotificationType
    ) -> Notification:
        """Send a notification to a user."""
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type
        )
        return await self._notification_repository.create(notification)


class MarkAsReadUseCase:
    """Use case for marking a notification as read."""
    
    def __init__(self, notification_repository: INotificationRepository):
        self._notification_repository = notification_repository
    
    async def execute(self, notification_id: str) -> Notification:
        """Mark a notification as read."""
        notification = await self._notification_repository.get_by_id(notification_id)
        if not notification:
            raise ValueError(f"Notification with id {notification_id} not found")
        
        notification.mark_as_read()
        return await self._notification_repository.update(notification)


class GetUserNotificationsUseCase:
    """Use case for getting user notifications."""
    
    def __init__(self, notification_repository: INotificationRepository):
        self._notification_repository = notification_repository
    
    async def execute(
        self,
        user_id: str,
        unread_only: bool = False
    ) -> List[Notification]:
        """Get notifications for a user."""
        return await self._notification_repository.get_by_user(user_id, unread_only)
