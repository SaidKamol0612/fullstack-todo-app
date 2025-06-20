from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import (
    GetTodoSchema,
    PostTodoSchema,
    PatchTodoSchema,
)
from .crud import (
    get_todos_db,
    get_todo_db,
    not_start_todo_db,
    activate_todo_db,
    archive_todo_db,
    add_todo_db,
    update_todo_db,
    delete_todo_db,
)

from core.db import db_helper

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/", response_model=list[GetTodoSchema])
async def get_todos(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    todos = await get_todos_db(session)
    return todos


@router.get("/{todo_id}", response_model=GetTodoSchema)
async def get_todo(
    session: AsyncSession = Depends(db_helper.session_getter), todo_id: int = None
):
    todo = await get_todo_db(session, todo_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ToDo with id {todo_id} not found",
        )

    return todo


@router.patch("/{todo_id}/not-start", response_model=GetTodoSchema)
async def not_start_todo(
    session: AsyncSession = Depends(db_helper.session_getter), todo_id: int = None
):
    todo = await get_todo_db(session, todo_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ToDo with id {todo_id} not found",
        )

    todo = await not_start_todo_db(session, todo)

    return todo


@router.patch("/{todo_id}/activate", response_model=GetTodoSchema)
async def activate_todo(
    session: AsyncSession = Depends(db_helper.session_getter), todo_id: int = None
):
    todo = await get_todo_db(session, todo_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ToDo with id {todo_id} not found",
        )

    todo = await activate_todo_db(session, todo)

    return todo


@router.patch("/{todo_id}/archive", response_model=GetTodoSchema)
async def archive_todo(
    session: AsyncSession = Depends(db_helper.session_getter), todo_id: int = None
):
    todo = await get_todo_db(session, todo_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ToDo with id {todo_id} not found",
        )

    todo = await archive_todo_db(session, todo)

    return todo


@router.post("/add", response_model=GetTodoSchema)
async def add_todo(
    session: AsyncSession = Depends(db_helper.session_getter),
    new_todo: PostTodoSchema = None,
):
    todo = await add_todo_db(session, new_todo)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return todo

@router.patch("/{todo_id}/update", response_model=GetTodoSchema)
async def update_todo(
    session: AsyncSession = Depends(db_helper.session_getter), 
    todo_id: int = None,
    upd: PatchTodoSchema = None,
):
    todo = await get_todo_db(session, todo_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ToDo with id {todo_id} not found",
        )

    todo = await update_todo_db(session, todo, upd)

    return todo

@router.delete('/{todo_id}/delete')
async def delete_todo(
    session: AsyncSession = Depends(db_helper.session_getter), 
    todo_id: int = None,
):
    todo = await get_todo_db(session, todo_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ToDo with id {todo_id} not found",
        )

    res = await delete_todo_db(session, todo)

    return {res: 'ToDo deleted successfully'}