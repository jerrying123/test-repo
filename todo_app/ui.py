"""NiceGUI frontend (mounted under /gui on the FastAPI app)."""

from __future__ import annotations

import asyncio

from nicegui import ui

from todo_app import crud, schemas
from todo_app.db import async_session_maker
from todo_app.settings import settings


def mount(fastapi_app) -> None:
    """Register pages and attach NiceGUI to the given FastAPI app."""

    @ui.page("/")
    async def todo_page():
        ui.label("Todo demo").classes("text-h5 q-mb-md")
        ui.label("REST API: /api/todos  ·  OpenAPI: /docs").classes("text-caption text-grey")

        show_done = ui.switch("Show completed", value=True)

        title_in = ui.input(label="Title").classes("w-full max-w-md")
        note_in = ui.textarea(label="Note (optional)").classes("w-full max-w-md")
        list_col = ui.column().classes("w-full max-w-xl gap-sm q-mt-md")

        async def paint():
            list_col.clear()
            async with async_session_maker() as session:
                todos = await crud.list_todos(session, include_done=show_done.value)
            with list_col:
                if not todos:
                    ui.label("No todos yet — add one above.").classes("text-grey")
                    return
                for t in todos:
                    with ui.card().classes("w-full"):
                        with ui.row().classes("items-start justify-between w-full no-wrap gap-md"):
                            with ui.column().classes("gap-xs"):
                                ui.label(t.title).classes("text-weight-medium")
                                if t.note:
                                    ui.label(t.note).classes("text-caption text-grey")
                                ui.label(
                                    f"{'Done' if t.done else 'Open'} · id={t.id}"
                                ).classes("text-caption")

                            with ui.column().classes("items-end gap-xs"):

                                def make_toggle(todo_id: int):
                                    async def handler():
                                        async with async_session_maker() as session:
                                            cur = await crud.get_todo(session, todo_id)
                                            if cur:
                                                await crud.patch_todo(
                                                    session,
                                                    todo_id,
                                                    schemas.TodoUpdate(done=not cur.done),
                                                )
                                        ui.notify("Updated")
                                        await paint()

                                    return handler

                                def make_delete(todo_id: int):
                                    async def handler():
                                        async with async_session_maker() as session:
                                            await crud.delete_todo(session, todo_id)
                                        ui.notify("Deleted")
                                        await paint()

                                    return handler

                                ui.button(
                                    "Mark undone" if t.done else "Mark done",
                                    on_click=make_toggle(t.id),
                                    color="secondary",
                                )
                                ui.button(
                                    icon="delete",
                                    on_click=make_delete(t.id),
                                    color="negative",
                                ).props("flat dense round")

        async def add_clicked():
            title = (title_in.value or "").strip()
            if not title:
                ui.notify("Enter a title", type="warning")
                return
            async with async_session_maker() as session:
                await crud.create_todo(
                    session,
                    schemas.TodoCreate(title=title, note=(note_in.value or "").strip()),
                )
            title_in.value = ""
            note_in.value = ""
            ui.notify("Created")
            await paint()

        ui.button("Add todo", on_click=add_clicked, color="primary")
        ui.button("Refresh", on_click=paint)

        show_done.on_value_change(lambda _: asyncio.create_task(paint()))

        await paint()

    ui.run_with(
        fastapi_app,
        mount_path="/gui",
        storage_secret=settings.nicegui_storage_secret,
    )
