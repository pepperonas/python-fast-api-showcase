"""Use cases for task service (application layer)."""

from typing import Optional, List
from datetime import datetime
from src.domain.task import Task, Project
from src.domain.value_objects import TaskStatus, TaskPriority
from src.domain.repository import ITaskRepository, IProjectRepository


class CreateTaskUseCase:
    """Use case for creating a new task."""
    
    def __init__(self, task_repository: ITaskRepository):
        self._task_repository = task_repository
    
    async def execute(
        self,
        title: str,
        created_by: str,
        description: Optional[str] = None,
        project_id: Optional[str] = None,
        priority: TaskPriority = TaskPriority.MEDIUM
    ) -> Task:
        """Create a new task."""
        task = Task(
            title=title,
            description=description,
            created_by=created_by,
            project_id=project_id,
            priority=priority
        )
        return await self._task_repository.create(task)


class UpdateTaskUseCase:
    """Use case for updating a task."""
    
    def __init__(self, task_repository: ITaskRepository):
        self._task_repository = task_repository
    
    async def execute(
        self,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        project_id: Optional[str] = None
    ) -> Task:
        """Update a task."""
        task = await self._task_repository.get_by_id(task_id)
        if not task:
            raise ValueError(f"Task with id {task_id} not found")
        
        if title is not None:
            task.update_title(title)
        if description is not None:
            task.update_description(description)
        if status is not None:
            task.change_status(status)
        if priority is not None:
            task.change_priority(priority)
        if project_id is not None:
            task._project_id = project_id
            task._updated_at = datetime.utcnow()
        
        return await self._task_repository.update(task)


class AssignTaskUseCase:
    """Use case for assigning a task to a user."""
    
    def __init__(self, task_repository: ITaskRepository):
        self._task_repository = task_repository
    
    async def execute(self, task_id: str, user_id: str) -> Task:
        """Assign a task to a user."""
        task = await self._task_repository.get_by_id(task_id)
        if not task:
            raise ValueError(f"Task with id {task_id} not found")
        
        task.assign_to(user_id)
        return await self._task_repository.update(task)


class GetTasksByProjectUseCase:
    """Use case for getting tasks by project."""
    
    def __init__(self, task_repository: ITaskRepository):
        self._task_repository = task_repository
    
    async def execute(
        self,
        project_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        """Get tasks by project ID."""
        return await self._task_repository.get_by_project(project_id, skip, limit)


class CreateProjectUseCase:
    """Use case for creating a new project."""
    
    def __init__(self, project_repository: IProjectRepository):
        self._project_repository = project_repository
    
    async def execute(
        self,
        name: str,
        created_by: str,
        description: Optional[str] = None
    ) -> Project:
        """Create a new project."""
        project = Project(
            name=name,
            description=description,
            created_by=created_by
        )
        return await self._project_repository.create(project)
