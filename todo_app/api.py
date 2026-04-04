from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from todo_app import crud, schemas
from todo_app.db import get_session

router = APIRouter()


@router.get("", response_model=list[schemas.TodoRead])
async def list_todos(
    session: AsyncSession = Depends(get_session),
    include_done: bool = Query(True, description="Include completed items"),
):
    return await crud.list_todos(session, include_done=include_done)


@router.post("", response_model=schemas.TodoRead, status_code=201)
async def create_todo(
    body: schemas.TodoCreate,
    session: AsyncSession = Depends(get_session),
):
    return await crud.create_todo(session, body)


@router.get("/{todo_id}", response_model=schemas.TodoRead)
async def get_todo(todo_id: int, session: AsyncSession = Depends(get_session)):
    t = await crud.get_todo(session, todo_id)
    if not t:
        raise HTTPException(status_code=404, detail="Todo not found")
    return t


@router.patch("/{todo_id}", response_model=schemas.TodoRead)
async def patch_todo(
    todo_id: int,
    body: schemas.TodoUpdate,
    session: AsyncSession = Depends(get_session),
):
    t = await crud.patch_todo(session, todo_id, body)
    if not t:
        raise HTTPException(status_code=404, detail="Todo not found")
    return t


@router.delete("/{todo_id}", status_code=204)
async def delete_todo(todo_id: int, session: AsyncSession = Depends(get_session)):
    ok = await crud.delete_todo(session, todo_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Todo not found")
