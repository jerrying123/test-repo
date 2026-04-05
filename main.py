"""
Run: docker compose up -d && uvicorn main:app --reload
API: http://127.0.0.1:8000/api/todos
Docs: http://127.0.0.1:8000/docs
UI: http://127.0.0.1:8000/gui
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from todo_app.api import router as todo_router
from todo_app.db import dispose_engine, init_db
from todo_app.ui import mount as mount_ui


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await dispose_engine()


app = FastAPI(title="Todo Demo — Postgres + FastAPI + NiceGUI", lifespan=lifespan)
app.include_router(todo_router, prefix="/api/todos", tags=["todos"])
mount_ui(app)
