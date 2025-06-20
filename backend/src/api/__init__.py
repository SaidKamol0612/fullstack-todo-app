__all__ = (
    'main_router'
)

from fastapi import APIRouter

from .todo import router as todos_router

main_router = APIRouter()

main_router.include_router(todos_router)