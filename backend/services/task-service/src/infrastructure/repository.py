"""Task repository implementation (infrastructure layer)."""

from typing import Optional, List
from sqlalchemy.orm import Session
from src.domain.task import Task, Project
from src.domain.repository import ITaskRepository, IProjectRepository
from src.infrastructure.models import TaskModel, ProjectModel


class TaskRepository(ITaskRepository):
    """SQLAlchemy implementation of task repository."""
    
    def __init__(self, db: Session):
        self._db = db
    
    async def create(self, task: Task) -> Task:
        """Create a new task."""
        db_task = TaskModel(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            project_id=task.project_id,
            assigned_to=task.assigned_to,
            created_by=task.created_by,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
        self._db.add(db_task)
        self._db.commit()
        self._db.refresh(db_task)
        return self._to_domain(db_task)
    
    async def get_by_id(self, task_id: str) -> Optional[Task]:
        """Get task by ID."""
        db_task = self._db.query(TaskModel).filter(TaskModel.id == task_id).first()
        return self._to_domain(db_task) if db_task else None
    
    async def get_by_project(self, project_id: str, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get tasks by project ID with pagination."""
        db_tasks = self._db.query(TaskModel)\
            .filter(TaskModel.project_id == project_id)\
            .offset(skip)\
            .limit(limit)\
            .all()
        return [self._to_domain(db_task) for db_task in db_tasks]
    
    async def get_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get tasks assigned to a user."""
        db_tasks = self._db.query(TaskModel)\
            .filter(TaskModel.assigned_to == user_id)\
            .offset(skip)\
            .limit(limit)\
            .all()
        return [self._to_domain(db_task) for db_task in db_tasks]
    
    async def update(self, task: Task) -> Task:
        """Update an existing task."""
        db_task = self._db.query(TaskModel).filter(TaskModel.id == task.id).first()
        if not db_task:
            raise ValueError(f"Task with id {task.id} not found")
        
        db_task.title = task.title
        db_task.description = task.description
        db_task.status = task.status
        db_task.priority = task.priority
        db_task.assigned_to = task.assigned_to
        db_task.updated_at = task.updated_at
        self._db.commit()
        self._db.refresh(db_task)
        return self._to_domain(db_task)
    
    async def delete(self, task_id: str) -> bool:
        """Delete a task."""
        db_task = self._db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not db_task:
            return False
        self._db.delete(db_task)
        self._db.commit()
        return True
    
    def _to_domain(self, db_task: TaskModel) -> Task:
        """Convert database model to domain entity."""
        return Task(
            task_id=db_task.id,
            title=db_task.title,
            description=db_task.description,
            status=db_task.status,
            priority=db_task.priority,
            project_id=db_task.project_id,
            assigned_to=db_task.assigned_to,
            created_by=db_task.created_by,
            created_at=db_task.created_at,
            updated_at=db_task.updated_at
        )


class ProjectRepository(IProjectRepository):
    """SQLAlchemy implementation of project repository."""
    
    def __init__(self, db: Session):
        self._db = db
    
    async def create(self, project: Project) -> Project:
        """Create a new project."""
        db_project = ProjectModel(
            id=project.id,
            name=project.name,
            description=project.description,
            created_by=project.created_by,
            created_at=project.created_at,
            updated_at=project.updated_at
        )
        self._db.add(db_project)
        self._db.commit()
        self._db.refresh(db_project)
        return self._to_domain(db_project)
    
    async def get_by_id(self, project_id: str) -> Optional[Project]:
        """Get project by ID."""
        db_project = self._db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
        return self._to_domain(db_project) if db_project else None
    
    async def get_by_user(self, user_id: str) -> List[Project]:
        """Get projects created by a user."""
        db_projects = self._db.query(ProjectModel)\
            .filter(ProjectModel.created_by == user_id)\
            .all()
        return [self._to_domain(db_project) for db_project in db_projects]
    
    async def update(self, project: Project) -> Project:
        """Update an existing project."""
        db_project = self._db.query(ProjectModel).filter(ProjectModel.id == project.id).first()
        if not db_project:
            raise ValueError(f"Project with id {project.id} not found")
        
        db_project.name = project.name
        db_project.description = project.description
        db_project.updated_at = project.updated_at
        self._db.commit()
        self._db.refresh(db_project)
        return self._to_domain(db_project)
    
    async def delete(self, project_id: str) -> bool:
        """Delete a project."""
        db_project = self._db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
        if not db_project:
            return False
        self._db.delete(db_project)
        self._db.commit()
        return True
    
    def _to_domain(self, db_project: ProjectModel) -> Project:
        """Convert database model to domain entity."""
        return Project(
            project_id=db_project.id,
            name=db_project.name,
            description=db_project.description,
            created_by=db_project.created_by,
            created_at=db_project.created_at,
            updated_at=db_project.updated_at
        )
