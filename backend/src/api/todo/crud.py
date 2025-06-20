from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import GetTodoSchema, PostTodoSchema, PatchTodoSchema

from core.db import models


async def get_todos_db(
    session: AsyncSession,
) -> list[GetTodoSchema]:
    stmt = select(models.Todo)
    res = await session.scalars(stmt)

    return [todo for todo in res]


async def get_todo_db(session: AsyncSession, todo_id: int) -> GetTodoSchema:
    stmt = select(models.Todo).where(models.Todo.id == todo_id)
    res = await session.scalar(stmt)

    return res if res else None


async def not_start_todo_db(
    session: AsyncSession, todo: GetTodoSchema
) -> GetTodoSchema:
    todo.status = models.TodoStatus.NOT_STARTED
    await session.commit()
    await session.refresh(todo)

    return todo


async def activate_todo_db(session: AsyncSession, todo: GetTodoSchema) -> GetTodoSchema:
    todo.status = models.TodoStatus.ACTIVE
    await session.commit()
    await session.refresh(todo)

    return todo


async def archive_todo_db(session: AsyncSession, todo: GetTodoSchema) -> GetTodoSchema:
    todo.status = models.TodoStatus.ARCHIVED
    await session.commit()
    await session.refresh(todo)

    return todo


async def add_todo_db(session: AsyncSession, new_todo: PostTodoSchema) -> GetTodoSchema:
    new_todo = models.Todo(**new_todo.model_dump())

    session.add(new_todo)
    await session.commit()
    await session.refresh(new_todo)

    return new_todo


async def update_todo_db(
    session: AsyncSession, todo: GetTodoSchema, upd: PatchTodoSchema
) -> GetTodoSchema:
    for key, value in upd.model_dump(exclude_unset=True).items():
        setattr(todo, key, value)

    await session.commit()
    await session.refresh(todo)

    return todo

async def delete_todo_db(
    session: AsyncSession, todo: GetTodoSchema
) -> bool:
    await session.delete(todo)
    await session.commit()
    
    return True
