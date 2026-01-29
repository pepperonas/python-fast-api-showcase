"""Notification repository implementation (infrastructure layer)."""

from typing import Optional, List
from sqlalchemy.orm import Session
from src.domain.notification import Notification
from src.domain.repository import INotificationRepository
from src.infrastructure.models import NotificationModel


class NotificationRepository(INotificationRepository):
    """SQLAlchemy implementation of notification repository."""
    
    def __init__(self, db: Session):
        self._db = db
    
    async def create(self, notification: Notification) -> Notification:
        """Create a new notification."""
        db_notification = NotificationModel(
            id=notification.id,
            user_id=notification.user_id,
            title=notification.title,
            message=notification.message,
            type=notification.type,
            read=notification.read,
            created_at=notification.created_at
        )
        self._db.add(db_notification)
        self._db.commit()
        self._db.refresh(db_notification)
        return self._to_domain(db_notification)
    
    async def get_by_id(self, notification_id: str) -> Optional[Notification]:
        """Get notification by ID."""
        db_notification = self._db.query(NotificationModel)\
            .filter(NotificationModel.id == notification_id)\
            .first()
        return self._to_domain(db_notification) if db_notification else None
    
    async def get_by_user(
        self,
        user_id: str,
        unread_only: bool = False
    ) -> List[Notification]:
        """Get notifications for a user."""
        query = self._db.query(NotificationModel)\
            .filter(NotificationModel.user_id == user_id)
        
        if unread_only:
            query = query.filter(NotificationModel.read == False)
        
        db_notifications = query.order_by(NotificationModel.created_at.desc()).all()
        return [self._to_domain(db_notification) for db_notification in db_notifications]
    
    async def update(self, notification: Notification) -> Notification:
        """Update an existing notification."""
        db_notification = self._db.query(NotificationModel)\
            .filter(NotificationModel.id == notification.id)\
            .first()
        if not db_notification:
            raise ValueError(f"Notification with id {notification.id} not found")
        
        db_notification.read = notification.read
        self._db.commit()
        self._db.refresh(db_notification)
        return self._to_domain(db_notification)
    
    async def mark_all_as_read(self, user_id: str) -> int:
        """Mark all notifications as read for a user."""
        count = self._db.query(NotificationModel)\
            .filter(NotificationModel.user_id == user_id)\
            .filter(NotificationModel.read == False)\
            .update({"read": True})
        self._db.commit()
        return count
    
    def _to_domain(self, db_notification: NotificationModel) -> Notification:
        """Convert database model to domain entity."""
        return Notification(
            notification_id=db_notification.id,
            user_id=db_notification.user_id,
            title=db_notification.title,
            message=db_notification.message,
            notification_type=db_notification.type,
            read=db_notification.read,
            created_at=db_notification.created_at
        )
