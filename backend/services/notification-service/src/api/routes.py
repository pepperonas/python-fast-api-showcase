"""FastAPI routes for notification service."""

import sys
from pathlib import Path

# Add backend directory to Python path for imports
backend_dir = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(backend_dir))

from fastapi import APIRouter, Depends, HTTPException, status, Query, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List
from shared.database import get_db
from shared.dto import NotificationDTO
from src.application.use_cases import (
    SendNotificationUseCase,
    MarkAsReadUseCase,
    GetUserNotificationsUseCase
)
from src.infrastructure.repository import NotificationRepository
from src.domain.notification import NotificationType
import json

router = APIRouter(prefix="/api/v1", tags=["notifications"])

# Simple WebSocket manager for real-time notifications
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
    
    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
    
    async def send_notification(self, user_id: str, notification: dict):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json(notification)

manager = ConnectionManager()


@router.get("/notifications", response_model=List[NotificationDTO])
async def get_notifications(
    unread_only: bool = Query(False),
    db: Session = Depends(get_db),
    current_user_id: str = "user-123"  # TODO: Get from auth token
):
    """Get notifications for current user."""
    repository = NotificationRepository(db)
    use_case = GetUserNotificationsUseCase(repository)
    
    notifications = await use_case.execute(current_user_id, unread_only)
    return [
        NotificationDTO(
            id=notification.id,
            user_id=notification.user_id,
            title=notification.title,
            message=notification.message,
            type=notification.type.value,
            read=notification.read,
            created_at=notification.created_at
        )
        for notification in notifications
    ]


@router.post("/notifications/{notification_id}/read", response_model=NotificationDTO)
async def mark_as_read(
    notification_id: str,
    db: Session = Depends(get_db)
):
    """Mark a notification as read."""
    repository = NotificationRepository(db)
    use_case = MarkAsReadUseCase(repository)
    
    try:
        notification = await use_case.execute(notification_id)
        return NotificationDTO(
            id=notification.id,
            user_id=notification.user_id,
            title=notification.title,
            message=notification.message,
            type=notification.type.value,
            read=notification.read,
            created_at=notification.created_at
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.websocket("/ws/notifications/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket endpoint for real-time notifications."""
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo or handle incoming messages if needed
            await websocket.send_json({"type": "ack", "message": "received"})
    except WebSocketDisconnect:
        manager.disconnect(user_id)
