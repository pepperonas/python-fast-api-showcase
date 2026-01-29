"""Task domain entity."""

from datetime import datetime
from typing import Optional
from uuid import uuid4
from .value_objects import TaskStatus, TaskPriority


class Task:
    """Task domain entity following DDD principles."""
    
    def __init__(
        self,
        title: str,
        created_by: str,
        status: TaskStatus = TaskStatus.TODO,
        priority: TaskPriority = TaskPriority.MEDIUM,
        description: Optional[str] = None,
        project_id: Optional[str] = None,
        assigned_to: Optional[str] = None,
        task_id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        if not title or len(title.strip()) == 0:
            raise ValueError("Task title cannot be empty")
        
        self._id = task_id or str(uuid4())
        self._title = title.strip()
        self._description = description
        self._status = status
        self._priority = priority
        self._project_id = project_id
        self._assigned_to = assigned_to
        self._created_by = created_by
        self._created_at = created_at or datetime.utcnow()
        self._updated_at = updated_at
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def description(self) -> Optional[str]:
        return self._description
    
    @property
    def status(self) -> TaskStatus:
        return self._status
    
    @property
    def priority(self) -> TaskPriority:
        return self._priority
    
    @property
    def project_id(self) -> Optional[str]:
        return self._project_id
    
    @property
    def assigned_to(self) -> Optional[str]:
        return self._assigned_to
    
    @property
    def created_by(self) -> str:
        return self._created_by
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def updated_at(self) -> Optional[datetime]:
        return self._updated_at
    
    def update_title(self, new_title: str) -> None:
        """Update task title."""
        if not new_title or len(new_title.strip()) == 0:
            raise ValueError("Task title cannot be empty")
        self._title = new_title.strip()
        self._updated_at = datetime.utcnow()
    
    def update_description(self, new_description: Optional[str]) -> None:
        """Update task description."""
        self._description = new_description
        self._updated_at = datetime.utcnow()
    
    def change_status(self, new_status: TaskStatus) -> None:
        """Change task status."""
        self._status = new_status
        self._updated_at = datetime.utcnow()
    
    def change_priority(self, new_priority: TaskPriority) -> None:
        """Change task priority."""
        self._priority = new_priority
        self._updated_at = datetime.utcnow()
    
    def assign_to(self, user_id: str) -> None:
        """Assign task to a user."""
        self._assigned_to = user_id
        self._updated_at = datetime.utcnow()
    
    def unassign(self) -> None:
        """Unassign task."""
        self._assigned_to = None
        self._updated_at = datetime.utcnow()


class Project:
    """Project aggregate root."""
    
    def __init__(
        self,
        name: str,
        created_by: str,
        description: Optional[str] = None,
        project_id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        if not name or len(name.strip()) == 0:
            raise ValueError("Project name cannot be empty")
        
        self._id = project_id or str(uuid4())
        self._name = name.strip()
        self._description = description
        self._created_by = created_by
        self._created_at = created_at or datetime.utcnow()
        self._updated_at = updated_at
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> Optional[str]:
        return self._description
    
    @property
    def created_by(self) -> str:
        return self._created_by
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def updated_at(self) -> Optional[datetime]:
        return self._updated_at
    
    def update_name(self, new_name: str) -> None:
        """Update project name."""
        if not new_name or len(new_name.strip()) == 0:
            raise ValueError("Project name cannot be empty")
        self._name = new_name.strip()
        self._updated_at = datetime.utcnow()
    
    def update_description(self, new_description: Optional[str]) -> None:
        """Update project description."""
        self._description = new_description
        self._updated_at = datetime.utcnow()
