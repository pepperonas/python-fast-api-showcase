"""Value objects for user domain."""

from pydantic import EmailStr, validator
from typing import Optional


class Email:
    """Email value object."""
    
    def __init__(self, value: str):
        self._value = EmailStr.validate(value)
    
    @property
    def value(self) -> str:
        return str(self._value)
    
    def __eq__(self, other):
        if not isinstance(other, Email):
            return False
        return self.value == other.value
    
    def __str__(self):
        return self.value


class Password:
    """Password value object with validation."""
    
    MIN_LENGTH = 8
    
    def __init__(self, value: str):
        if len(value) < self.MIN_LENGTH:
            raise ValueError(f"Password must be at least {self.MIN_LENGTH} characters long")
        self._value = value
    
    @property
    def value(self) -> str:
        return self._value
    
    def __eq__(self, other):
        if not isinstance(other, Password):
            return False
        return self.value == other.value
