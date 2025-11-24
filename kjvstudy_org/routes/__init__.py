"""Routes package for KJV Study."""
from fastapi import APIRouter

from .api import router as api_router

__all__ = ['api_router']
