"""Unit tests for task domain."""

import pytest
from src.domain.task import Task, Project
from src.domain.value_objects import TaskStatus, TaskPriority


def test_task_creation():
    """Test task entity creation."""
    task = Task(
        title="Test Task",
        created_by="user-123",
        description="Test description",
        priority=TaskPriority.HIGH
    )
    
    assert task.title == "Test Task"
    assert task.status == TaskStatus.TODO
    assert task.priority == TaskPriority.HIGH
    assert task.id is not None


def test_task_status_change():
    """Test changing task status."""
    task = Task(
        title="Test Task",
        created_by="user-123"
    )
    
    task.change_status(TaskStatus.IN_PROGRESS)
    assert task.status == TaskStatus.IN_PROGRESS
    assert task.updated_at is not None


def test_project_creation():
    """Test project aggregate creation."""
    project = Project(
        name="Test Project",
        created_by="user-123",
        description="Test description"
    )
    
    assert project.name == "Test Project"
    assert project.id is not None
