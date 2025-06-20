import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from core.db import db_helper
from core.config import settings

from api import main_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup

    yield
    # shutdown
    await db_helper.dispose()


app = FastAPI(
    default_response_class=ORJSONResponse,
    title=settings.api.title,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"msg": "Welcome to ToDo API with Postgres DB"}


app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run("run:app", host=settings.run.host, port=settings.run.port, reload=True)
