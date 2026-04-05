from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from todo_app import schemas
from todo_app.models import Todo


async def list_todos(session: AsyncSession, *, include_done: bool = True) -> list[Todo]:
    q = select(Todo).order_by(Todo.created_at.desc())
    if not include_done:
        q = q.where(Todo.done.is_(False))
    r = await session.execute(q)
    return list(r.scalars().all())


async def get_todo(session: AsyncSession, todo_id: int) -> Todo | None:
    r = await session.execute(select(Todo).where(Todo.id == todo_id))
    return r.scalar_one_or_none()


async def create_todo(session: AsyncSession, data: schemas.TodoCreate) -> Todo:
    t = Todo(title=data.title, note=data.note or "", done=False)
    session.add(t)
    await session.commit()
    await session.refresh(t)
    return t


async def patch_todo(session: AsyncSession, todo_id: int, data: schemas.TodoUpdate) -> Todo | None:
    t = await get_todo(session, todo_id)
    if not t:
        return None
    if data.title is not None:
        t.title = data.title
    if data.note is not None:
        t.note = data.note
    if data.done is not None:
        t.done = data.done
    await session.commit()
    await session.refresh(t)
    return t


async def delete_todo(session: AsyncSession, todo_id: int) -> bool:
    t = await get_todo(session, todo_id)
    if not t:
        return False
    await session.delete(t)
    await session.commit()
    return True
