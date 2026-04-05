"""DB layer only — run after `demo/todo-1-api` for REST, `demo/todo-2-nicegui` for UI."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from todo_app.db import dispose_engine, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await dispose_engine()


app = FastAPI(title="Todo Demo — DB layer (demo/todo-0-postgres)", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok", "layer": "postgres_sqlalchemy_models"}
