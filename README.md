# test-repo — nugit demo (todo app)

Sandbox repo for **stacked PRs** with the **nugit** CLI. This example is a small **FastAPI** REST API, **PostgreSQL** (via Docker), and a **NiceGUI** web UI for a generic todo list.

## Branches (linear stack)

Create PRs in order (each branch is based on the previous) to mirror a real nugit stack:

| Branch | What it adds |
|--------|----------------|
| `main` | Tooling only: Docker Compose Postgres, `requirements.txt`, `.env.example`, this README |
| `demo/todo-0-postgres` | SQLAlchemy async + `Todo` model + DB init (`todo_app/db.py`, `models.py`, `settings.py`) + slim `main.py` (`/health` only) |
| `demo/todo-1-api` | Pydantic schemas, CRUD helpers, FastAPI `/api/todos` router + OpenAPI at `/docs` |
| `demo/todo-2-nicegui` | NiceGUI pages mounted at **`/gui`**, sharing the same database |

After pushing branches and opening PRs on GitHub:

```bash
export NUGIT_USER_TOKEN=ghp_...
nugit init
nugit stack add --pr <bottom> <middle> <top>   # PR numbers bottom → top
nugit stack propagate --push
nugit stack view
```

Replace `repo_full_name` / `created_by` in `.nugit/stack.json` if `nugit init` does not match your fork.

## Run locally

```bash
cd test-repo
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # optional: edit DATABASE_URL
docker compose up -d
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- **Swagger:** http://127.0.0.1:8000/docs  
- **Todos API:** http://127.0.0.1:8000/api/todos  
- **NiceGUI UI:** http://127.0.0.1:8000/gui  

Default DB URL matches `docker-compose.yml` (`todo` / `todo` / `todoapp` on port **5432**).

## Layout

```
todo_app/
  settings.py   # pydantic-settings (DATABASE_URL, NiceGUI secret)
  db.py         # async engine, session, init_db
  models.py     # Todo table
  schemas.py    # Pydantic I/O models
  crud.py       # async DB operations
  api.py        # FastAPI router
  ui.py         # NiceGUI mount + todo page
main.py         # FastAPI app + lifespan + includes router + mounts UI
docker-compose.yml
```

This is **dummy / teaching code**: minimal validation, no migrations (tables created on startup), not production-hardened.
