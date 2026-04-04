# test-repo — nugit demo (todo app)

**Public example:** [github.com/jerrying123/test-repo](https://github.com/jerrying123/test-repo)

Sandbox repo for **stacked PRs** with the **nugit** CLI. This example is a small **FastAPI** REST API, **PostgreSQL** (via Docker), and a **NiceGUI** web UI for a generic todo list.

You can use this repo **only on GitHub** (browse branches and PRs in the browser) or follow **§ Explore with the nugit CLI** below to exercise **`stack list`**, **`view`** / **`stack view`**, and related commands against the **same** public `owner/repo` without forking—**read-only** exploration only. Changing stack state or opening PRs requires your own fork or maintainer access.

---

## Explore with the nugit CLI (public repo)

These commands target **`jerrying123/test-repo`** explicitly. You do **not** need a local clone of this repo for them (any directory is fine).

**Token:** For **read-only** commands against this **public** repo, nugit can omit **`NUGIT_USER_TOKEN`** and use **unauthenticated** GitHub `GET`s (roughly **60 requests/hour** per IP). Set a [PAT](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) for **`auth whoami`**, **posting comments**, **private** repos, or **smoother** browsing.

```bash
# Install the published CLI (or use a clone of github.com/jerrying123/nugit and run ./cli/src/nugit.js)
npm install -g nugit-cli

# Optional — higher rate limits and write actions
export NUGIT_USER_TOKEN=ghp_your_token_here
# nugit auth whoami   # verify token (needs NUGIT_USER_TOKEN)

# Open PRs in this demo repo (read-only; works without a token on public repos)
nugit prs list --repo jerrying123/test-repo

# Scan open PR heads for .nugit/stack.json and list discovered stacks (deduped by tip)
nugit stack list --repo jerrying123/test-repo

# If your nugit config uses lazy discovery, force a full scan for this run:
NUGIT_STACK_DISCOVERY_FULL=1 nugit stack list --repo jerrying123/test-repo

# Interactive TUI: same as `nugit stack view` — works on public repos without a token (reads only)
nugit view --repo jerrying123/test-repo --ref demo/todo-2-nicegui

# Non-interactive peek at the same stack file + PR metadata counts
nugit view --repo jerrying123/test-repo --ref demo/todo-2-nicegui --no-tui
```

**What you are seeing:** **`stack list`** shows how nugit **discovers** stacks from multiple PR heads. **`view --repo … --ref …`** shows how it loads **`.nugit/stack.json`** from a **remote ref** and joins it with GitHub PR/issue data. If **`prs`** in that file is still empty, the viewer lists no stacked PRs until maintainers (or you on a fork) run **`nugit stack add`** and push.

**Optional clone** (run app locally *or* use cwd-based nugit defaults):

```bash
git clone https://github.com/jerrying123/test-repo.git
cd test-repo
git checkout demo/todo-2-nicegui   # full app + template .nugit/stack.json
nugit stack show                    # prints local .nugit/stack.json
```

---

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

On **`demo/todo-2-nicegui`**, `.nugit/stack.json` is a template with **`repo_full_name`** `jerrying123/test-repo` and empty **`prs`**. Edit it to match your GitHub login/repo, or run **`nugit init`** and **`nugit stack add --pr …`** after you open the three stacked PRs.

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
