"""REST API layer — add NiceGUI on branch demo/todo-2-nicegui."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from todo_app.api import router as todo_router
from todo_app.db import dispose_engine, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await dispose_engine()


app = FastAPI(title="Todo Demo — API layer (demo/todo-1-api)", lifespan=lifespan)
app.include_router(todo_router, prefix="/api/todos", tags=["todos"])


@app.get("/health")
async def health():
    return {"status": "ok", "layer": "fastapi_crud"}
