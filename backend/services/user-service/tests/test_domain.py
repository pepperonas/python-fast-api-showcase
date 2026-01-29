"""Unit tests for user domain."""

import pytest
from src.domain.user import User
from src.domain.value_objects import Email, Password


def test_user_creation():
    """Test user entity creation."""
    email = Email("test@example.com")
    user = User(
        email=email,
        full_name="Test User",
        password_hash="hashed_password"
    )
    
    assert user.email == email
    assert user.full_name == "Test User"
    assert user.id is not None


def test_user_update_full_name():
    """Test updating user full name."""
    email = Email("test@example.com")
    user = User(
        email=email,
        full_name="Test User",
        password_hash="hashed_password"
    )
    
    user.update_full_name("Updated Name")
    assert user.full_name == "Updated Name"
    assert user.updated_at is not None


def test_password_validation():
    """Test password value object validation."""
    # Valid password
    password = Password("validpassword123")
    assert password.value == "validpassword123"
    
    # Invalid password (too short)
    with pytest.raises(ValueError):
        Password("short")


def test_email_value_object():
    """Test email value object."""
    email1 = Email("test@example.com")
    email2 = Email("test@example.com")
    email3 = Email("other@example.com")
    
    assert email1 == email2
    assert email1 != email3
    assert str(email1) == "test@example.com"
