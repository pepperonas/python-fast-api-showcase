"""Event schemas for domain events."""

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel


class EventType(str, Enum):
    """Domain event types."""
    TASK_CREATED = "task.created"
    TASK_UPDATED = "task.updated"
    TASK_ASSIGNED = "task.assigned"
    TASK_COMPLETED = "task.completed"
    USER_REGISTERED = "user.registered"


class DomainEvent(BaseModel):
    """Base domain event."""
    event_type: EventType
    aggregate_id: str
    occurred_at: datetime
    metadata: Optional[dict] = None
    
    class Config:
        use_enum_values = True


class TaskCreatedEvent(DomainEvent):
    """Event emitted when a task is created."""
    task_id: str
    project_id: Optional[str]
    created_by: str


class TaskUpdatedEvent(DomainEvent):
    """Event emitted when a task is updated."""
    task_id: str
    changes: dict


class TaskAssignedEvent(DomainEvent):
    """Event emitted when a task is assigned."""
    task_id: str
    assigned_to: str
    assigned_by: str
