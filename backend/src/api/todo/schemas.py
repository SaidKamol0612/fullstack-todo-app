from pydantic import BaseModel

from core.db import models


class BaseTodoSchema(BaseModel):
    title: str
    description: str | None = None


class GetTodoSchema(BaseTodoSchema):
    id: int
    status: models.TodoStatus


class PostTodoSchema(BaseTodoSchema):
    pass

class PatchTodoSchema(BaseTodoSchema):
    title: str | None = None
