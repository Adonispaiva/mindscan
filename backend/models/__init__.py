"""
Backend Models Package
Expose ORM models for external imports.

Exemplo suportado:
    from backend.models import User
"""

from __future__ import annotations

# Import explícito do ORM model "User"
from .user import User

__all__ = [
    "User",
]
