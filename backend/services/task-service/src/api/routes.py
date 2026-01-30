"""FastAPI routes for task service."""

import sys
from pathlib import Path

# Add backend directory to Python path for imports
backend_dir = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(backend_dir))

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from shared.database import get_db
from shared.dto import TaskDTO, ProjectDTO
from src.application.use_cases import (
    CreateTaskUseCase,
    UpdateTaskUseCase,
    AssignTaskUseCase,
    GetTasksByProjectUseCase,
    CreateProjectUseCase
)
from src.infrastructure.repository import TaskRepository, ProjectRepository
from src.domain.value_objects import TaskStatus, TaskPriority
from src.api.dependencies import get_current_user_id

router = APIRouter(prefix="/api/v1", tags=["tasks"])


class CreateTaskRequest(BaseModel):
    """Request model for creating a task."""
    title: str
    description: Optional[str] = None
    project_id: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM


class UpdateTaskRequest(BaseModel):
    """Request model for updating a task."""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    project_id: Optional[str] = None


class AssignTaskRequest(BaseModel):
    """Request model for assigning a task."""
    user_id: str


class CreateProjectRequest(BaseModel):
    """Request model for creating a project."""
    name: str
    description: Optional[str] = None


@router.get("/tasks", response_model=List[TaskDTO])
async def get_all_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id)
):
    """Get all tasks for current user (created by or assigned to)."""
    repository = TaskRepository(db)
    # Get tasks created by user or assigned to user
    from src.infrastructure.models import TaskModel
    from sqlalchemy import or_
    db_tasks = db.query(TaskModel)\
        .filter(or_(TaskModel.created_by == current_user_id, TaskModel.assigned_to == current_user_id))\
        .offset(skip)\
        .limit(limit)\
        .all()
    tasks = [repository._to_domain(db_task) for db_task in db_tasks]
    return [
        TaskDTO(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status.value,
            priority=task.priority.value,
            project_id=task.project_id,
            assigned_to=task.assigned_to,
            created_by=task.created_by,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
        for task in tasks
    ]


@router.post("/tasks", response_model=TaskDTO, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: CreateTaskRequest,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id)
):
    """Create a new task."""
    repository = TaskRepository(db)
    use_case = CreateTaskUseCase(repository)
    
    try:
        task = await use_case.execute(
            title=request.title,
            description=request.description,
            project_id=request.project_id,
            created_by=current_user_id,
            priority=request.priority
        )
        return TaskDTO(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status.value,
            priority=task.priority.value,
            project_id=task.project_id,
            assigned_to=task.assigned_to,
            created_by=task.created_by,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/tasks/{task_id}", response_model=TaskDTO)
async def get_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id)
):
    """Get task by ID."""
    repository = TaskRepository(db)
    task = await repository.get_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return TaskDTO(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status.value,
        priority=task.priority.value,
        project_id=task.project_id,
        assigned_to=task.assigned_to,
        created_by=task.created_by,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


@router.put("/tasks/{task_id}", response_model=TaskDTO)
async def update_task(
    task_id: str,
    request: UpdateTaskRequest,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id)
):
    """Update a task."""
    repository = TaskRepository(db)
    use_case = UpdateTaskUseCase(repository)
    
    try:
        task = await use_case.execute(
            task_id=task_id,
            title=request.title,
            description=request.description,
            status=request.status,
            priority=request.priority,
            project_id=request.project_id
        )
        return TaskDTO(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status.value,
            priority=task.priority.value,
            project_id=task.project_id,
            assigned_to=task.assigned_to,
            created_by=task.created_by,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/tasks/{task_id}/assign", response_model=TaskDTO)
async def assign_task(
    task_id: str,
    request: AssignTaskRequest,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id)
):
    """Assign a task to a user."""
    repository = TaskRepository(db)
    use_case = AssignTaskUseCase(repository)
    
    try:
        task = await use_case.execute(task_id, request.user_id)
        return TaskDTO(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status.value,
            priority=task.priority.value,
            project_id=task.project_id,
            assigned_to=task.assigned_to,
            created_by=task.created_by,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/projects/{project_id}/tasks", response_model=List[TaskDTO])
async def get_tasks_by_project(
    project_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id)
):
    """Get tasks by project ID with pagination."""
    repository = TaskRepository(db)
    use_case = GetTasksByProjectUseCase(repository)
    
    tasks = await use_case.execute(project_id, skip, limit)
    return [
        TaskDTO(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status.value,
            priority=task.priority.value,
            project_id=task.project_id,
            assigned_to=task.assigned_to,
            created_by=task.created_by,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
        for task in tasks
    ]


@router.get("/projects", response_model=List[ProjectDTO])
async def get_all_projects(
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id)
):
    """Get all projects for current user."""
    repository = ProjectRepository(db)
    projects = await repository.get_by_user(current_user_id)
    return [
        ProjectDTO(
            id=project.id,
            name=project.name,
            description=project.description,
            created_by=project.created_by,
            created_at=project.created_at,
            updated_at=project.updated_at
        )
        for project in projects
    ]


@router.post("/projects", response_model=ProjectDTO, status_code=status.HTTP_201_CREATED)
async def create_project(
    request: CreateProjectRequest,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id)
):
    """Create a new project."""
    repository = ProjectRepository(db)
    use_case = CreateProjectUseCase(repository)
    
    try:
        project = await use_case.execute(
            name=request.name,
            description=request.description,
            created_by=current_user_id
        )
        return ProjectDTO(
            id=project.id,
            name=project.name,
            description=project.description,
            created_by=project.created_by,
            created_at=project.created_at,
            updated_at=project.updated_at
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/projects/{project_id}", response_model=ProjectDTO)
async def get_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id)
):
    """Get project by ID."""
    repository = ProjectRepository(db)
    project = await repository.get_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return ProjectDTO(
        id=project.id,
        name=project.name,
        description=project.description,
        created_by=project.created_by,
        created_at=project.created_at,
        updated_at=project.updated_at
    )
