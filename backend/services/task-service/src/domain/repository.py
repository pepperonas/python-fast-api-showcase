"""Task repository interface (domain layer)."""

from abc import ABC, abstractmethod
from typing import Optional, List
from .task import Task, Project


class ITaskRepository(ABC):
    """Interface for task repository."""
    
    @abstractmethod
    async def create(self, task: Task) -> Task:
        """Create a new task."""
        pass
    
    @abstractmethod
    async def get_by_id(self, task_id: str) -> Optional[Task]:
        """Get task by ID."""
        pass
    
    @abstractmethod
    async def get_by_project(self, project_id: str, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get tasks by project ID with pagination."""
        pass
    
    @abstractmethod
    async def get_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get tasks assigned to a user."""
        pass
    
    @abstractmethod
    async def update(self, task: Task) -> Task:
        """Update an existing task."""
        pass
    
    @abstractmethod
    async def delete(self, task_id: str) -> bool:
        """Delete a task."""
        pass


class IProjectRepository(ABC):
    """Interface for project repository."""
    
    @abstractmethod
    async def create(self, project: Project) -> Project:
        """Create a new project."""
        pass
    
    @abstractmethod
    async def get_by_id(self, project_id: str) -> Optional[Project]:
        """Get project by ID."""
        pass
    
    @abstractmethod
    async def get_by_user(self, user_id: str) -> List[Project]:
        """Get projects created by a user."""
        pass
    
    @abstractmethod
    async def update(self, project: Project) -> Project:
        """Update an existing project."""
        pass
    
    @abstractmethod
    async def delete(self, project_id: str) -> bool:
        """Delete a project."""
        pass
